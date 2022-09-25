import {join, omitBy, reduce, some, trim, uniq, uniqBy} from "lodash-es";
import {parseString} from "@fast-csv/parse";
import {writeFile, readFile} from "fs/promises";
import {existsSync, mkdirSync} from "fs";
import {spawnSync} from "child_process"
import {pascalCase} from "./common";
import {findWeapon} from "./domain_weapon";
import {findArtifactSet} from "./domain_artifact";
import {FightProp} from "./openconfig";
import {dirname} from "path";

const statsMap: Record<string, string> = {
    "HP%": "FIGHT_PROP_HP_PERCENT",
    "ATK%": "FIGHT_PROP_ATTACK_PERCENT",
    "DEF%": "FIGHT_PROP_DEFENSE_PERCENT",
    "Flat HP": "FIGHT_PROP_HP",
    HP: "FIGHT_PROP_HP",
    "Flat ATK": "FIGHT_PROP_ATTACK",
    ATK: "FIGHT_PROP_ATTACK",
    "Flat DEF": "FIGHT_PROP_DEFENSE",
    DEF: "FIGHT_PROP_DEFENSE",

    "Elemental Mastery": "FIGHT_PROP_ELEMENT_MASTERY",
    EM: "FIGHT_PROP_ELEMENT_MASTERY",
    "Energy Recharge": "FIGHT_PROP_CHARGE_EFFICIENCY",
    "ER%": "FIGHT_PROP_CHARGE_EFFICIENCY",
    "Crit Rate": "FIGHT_PROP_CRITICAL",
    "Crit DMG": "FIGHT_PROP_CRITICAL_HURT",
    // hack
    DMG: "FIGHT_PROP_CRITICAL_HURT",

    "Healing Bonus": "FIGHT_PROP_HEAL_ADD",
    "Healing Bonus%": "FIGHT_PROP_HEAL_ADD",

    "Pyro DMG": "FIGHT_PROP_FIRE_ADD_HURT",
    "Hydro DMG": "FIGHT_PROP_WATER_ADD_HURT",
    "Geo DMG": "FIGHT_PROP_ROCK_ADD_HURT",
    "Cryo DMG": "FIGHT_PROP_ICE_ADD_HURT",
    "Electro DMG": "FIGHT_PROP_ELEC_ADD_HURT",
    "Anemo DMG": "FIGHT_PROP_WIND_ADD_HURT",
    "Dendro DMG": "FIGHT_PROP_GRASS_ADD_HURT",
    "Physical DMG": "FIGHT_PROP_PHYSICAL_ADD_HURT",
    "Phys DMG": "FIGHT_PROP_PHYSICAL_ADD_HURT",
};

const resolvePropTypes = (s: string, mustPercent = false): string[] => {
    return reduce(
        trim(s, "*").split("/"),
        (ret: string[], s: string) => {
            let f =
                statsMap[s.trim()] ||
                statsMap[trim(s.trim(), "*")] ||
                statsMap[s.trim().replace("Damage", "DMG")] ||
                statsMap[s.trim().replace("Attack", "ATK")] ||
                statsMap[s.trim().replace("Defence", "DEF")];

            if (f) {
                if (["FIGHT_PROP_HP", "FIGHT_PROP_ATTACK", "FIGHT_PROP_DEFENSE"].includes(f) && mustPercent) {
                    f = `${f}_PERCENT`;
                }
                return [...ret, f];
            }

            console.warn(`unknown prop name "${s}" ${f}`);

            return ret;
        },
        [],
    );
};

const chooseTwo = (list: string[]) => {
    const pairs: string[][] = [];

    for (let i = 0; i < list.length; i++) {
        for (let j = i + 1; j < list.length; j++) {
            pairs.push([list[i], list[j]]);
        }
    }

    return pairs;
};

const formatSkillType = (v: string) => {
    return (
        {
            BURST: "Q",
            NORMALATTACK: "A",
            SKILL: "E",
        } as any
    )[pascalCase(trim(v, "*").trim()).toUpperCase()];
};

const weaponAliases: { [k: string]: string } = {
    "Skyrider's Greatsword": "Skyrider Greatsword",
    Wavebreaker: "Wavebreaker's Fin",
    "Aquilla Favonia": "Aquila Favonia",
    "Viridescent Hunt": "The Viridescent Hunt",
    "Anemona Kageuchi": "Amenoma Kageuchi",
    // "Solar Pearl R4": "Solar Pearl",
    // "Festering Desire R5": "Festering Desire",
    // "Amenoma Kageuchi [R3+]": "Amenoma Kageuchi",
};

const artifactSetAliases: { [k: string]: string } = {
    "Emblem of Severed Fates": "Emblem of Severed Fate",
    "Maiden's Beloved": "Maiden Beloved",
    "Lavawalkers Epiphany": "Lavawalker",
    "Tenacity of the Milelith": "Tenacity of the Millelith",
    Thundersoothers: "Thundersoother",
    Instructors: "Instructor",
    "Physical DMG +25% set": "Pale Flame",
};

const characterBuild = (name: string, b: any) => {
    function completeArtifactAffixPropTypes(list: string[]) {
        return uniq(
            reduce(
                list,
                (ret, f) => {
                    if (f == "FIGHT_PROP_HP_PERCENT") {
                        return [...ret, f, "FIGHT_PROP_HP"];
                    }
                    if (f == "FIGHT_PROP_ATTACK_PERCENT") {
                        return [...ret, f, "FIGHT_PROP_ATTACK"];
                    }
                    if (f == "FIGHT_PROP_DEFENSE_PERCENT") {
                        return [...ret, f, "FIGHT_PROP_DEFENSE"];
                    }
                    return [...ret, f];
                },
                [] as string[],
            ),
        );
    }

    return {
        Recommended: b.recommended,
        Role: b.role,
        Weapons: b.weapons
            .map((ids: string[]) =>
                ids
                    .map((id: string) => {
                        const found = findWeapon(pascalCase(weaponAliases[id] || id));
                        if (found) {
                            return found.Name.CHS;
                        }
                        console.warn(`${name} missing weapon "${id}"`);
                        return "";
                    })
                    .filter((v: string) => v),
            )
            .filter((list: string) => list.length > 0),
        ArtifactMainPropTypes: {
            EQUIP_SHOES: resolvePropTypes(b.mainStats.sands, true),
            EQUIP_RING: resolvePropTypes(b.mainStats.goblet, true),
            EQUIP_DRESS: resolvePropTypes(b.mainStats.circlet, true),
        },
        ArtifactAffixPropTypes: completeArtifactAffixPropTypes(
            reduce(b.subStats, (ret: string[], s: string) => [...ret, ...resolvePropTypes(s)], []),
        ),
        ArtifactSetPairs: uniqBy(
            b.artifacts.reduce((ret: string[][], sets: string[]) => {
                const pair = sets
                    .map((setName) => {
                        const found = findArtifactSet(pascalCase(artifactSetAliases[setName] || setName));
                        if (found) {
                            return found.Name.CHS;
                        }
                        if ("18AtkSet" === pascalCase(artifactSetAliases[setName] || setName)) {
                            return "角斗士的终幕礼";
                        }
                        if ("20ErSet" === pascalCase(artifactSetAliases[setName] || setName)) {
                            return "绝缘之旗印";
                        }
                        console.warn(`${name} missing artifact set "${setName}"`);
                        return null;
                    })
                    .filter((s) => s) as string[];

                if (pair.length > 2) {
                    return [...ret, ...chooseTwo(pair)];
                }

                return [...ret, pair];
            }, []),
            (s: string[]) => s.join("/"),
        ),
        SkillPriority: b.talent.map((v: string) =>
            v
                .split("/")
                .map(formatSkillType)
                .filter((v) => v),
        ),
    };
};

const exportURL = `https://docs.google.com/spreadsheets/d/1gNxZ2xab1J6o1TuNVWMeLOZ7TPOqrsf3SshP5DLvKzI/export?format=csv`;

enum Grid {
    Dendro = 1468017260,
    Anemo = 653464458,
    Geo = 1780570478,
    Electro = 408609723,
    Cryo = 1169063456,
    Hydro = 1354385732,
    Pyro = 954718212,
}

const loadOrSync = async (g: Grid) => {
    const file = `./.tmp/${Grid[g]}-${g}.csv`;
    if (!existsSync(file)) {
        console.log(`fetching ${Grid[g]} ${exportURL}&gid=${g}`)
        await mkdirSync(dirname(file), {recursive: true});

        spawnSync("curl", ["-qL", "-o", file, `${exportURL}&gid=${g}`], {
            cwd: process.cwd(),
            env: process.env,
            stdio: 'inherit',
        });
    }
    return String(await readFile(file));
};

const fromCSV = async (csv: string, grid: Grid) => {
    const ret: { [k: string]: any } = {};

    const pickList = (cell: string) => {
        return cell
            .split(/\d+\. ?/)
            .map((v) => trim(v))
            .filter((v: string) => v && !(v.startsWith("*") || v.startsWith("(") || v.endsWith(".")))
            .map((w: string) =>
                w
                    .split(/(~?=)|\([24]\)|\/|(\n)/)
                    .filter((v) => trim(v))
                    .map((v) => v.replace(/(\d+\. ?)?([^(\[]+)(.+)?(R[1-5]\+?)?/, "$2").trim())
                    .filter((v) => v && !(v.startsWith("*") || v.startsWith("(") || v.startsWith("[") || v === "S1" || v == "~=")),
            );
    };

    const pickMainStats = (cell: string) => {
        return cell
            .split("\n")
            .map((v) => trim(v.trim(), "*"))
            .filter((v: string) => v && !(v.startsWith("*") || v.startsWith("(") || v.endsWith(".")))
            .reduce((ret, v: string) => {
                const parts = v.split(/[-:]/);

                if (parts.length !== 2) {
                    return ret;
                }

                return {
                    ...ret,
                    [parts[0].trim().toLowerCase()]: parts[1].trim(),
                };
            }, {});
    };

    return new Promise<{ [k: string]: any }>((resolve) => {
        let scope = "";
        let partIdx = 0;

        parseString(csv)
            .on("end", () => {
                resolve(ret);
            })
            .on("data", (row) => {
                if (row.indexOf("EQUIPMENT") > -1 || row.indexOf("EQUIPMENTS") > -1) {
                    scope = row[1];

                    switch (scope.toUpperCase()) {
                        case "CHILDE":
                            scope = "tartaglia";
                            break;
                        case "KOKOMI":
                            scope = "sangonomiya_kokomi";
                            break;
                        case "TRAVELER":
                            scope = `${scope} ${Grid[grid]}`;
                            break;
                    }

                    partIdx = 0;
                }

                if (scope != "" && partIdx >= 2) {
                    if (row[1] !== "") {
                        // scope done
                        scope = "";
                        return;
                    }

                    const role = row[2].replace("✩", "").split("\n")[0].trim();
                    const recommended = row[2].indexOf("✩") > -1;

                    if (!role) {
                        return;
                    }

                    ret[pascalCase(scope)] = [
                        ...(ret[pascalCase(scope)] || []),
                        characterBuild(scope, {
                            recommended: recommended,
                            name: scope,
                            role: role,
                            weapons: pickList(row[3]),
                            artifacts: pickList(row[4]),
                            mainStats: pickMainStats(row[5]),
                            subStats: pickList(row[6]).flat(),
                            talent: pickList(row[7]).flat(),
                        }),
                    ];
                }

                partIdx++;
            });
    });
};

const defaultRole = (role: string, weapon: string, artifact: string[], fps: [FightProp, FightProp, FightProp], skills: string[]) => ({
    Recommended: false,
    Role: role,
    Weapons: [
        [weapon]
    ],
    ArtifactMainPropTypes: {
        EQUIP_SHOES: [FightProp[fps[0]]],
        EQUIP_RING: [FightProp[fps[1]]],
        EQUIP_DRESS: [FightProp[fps[2]]],
    },
    ArtifactAffixPropTypes: [
        FightProp[fps[0]],
        FightProp[fps[2]],
    ].filter((v) => v !== FightProp[FightProp.FIGHT_PROP_HEAL_ADD]),
    ArtifactSetPairs: [artifact],
    SkillPriority: skills.map((s) => [s]),
})

export let Builds: { [key: string]: Array<ReturnType<typeof characterBuild>> } = {
    ShikanoinHeizou: [
        defaultRole("DPS", "天空之卷", ["翠绿之影"], [
            FightProp.FIGHT_PROP_ATTACK_PERCENT,
            FightProp.FIGHT_PROP_WIND_ADD_HURT,
            FightProp.FIGHT_PROP_CRITICAL,
        ], ["E", "Q"])
    ],
    TravelerDendro: [
        defaultRole("DPS", "西风剑", ["深林的记忆"], [
            FightProp.FIGHT_PROP_ATTACK_PERCENT,
            FightProp.FIGHT_PROP_GRASS_ADD_HURT,
            FightProp.FIGHT_PROP_CRITICAL,
        ], ["Q", "E"])
    ],
    Collei: [
        defaultRole("DPS", "西风猎弓", ["深林的记忆"], [
            FightProp.FIGHT_PROP_ATTACK_PERCENT,
            FightProp.FIGHT_PROP_GRASS_ADD_HURT,
            FightProp.FIGHT_PROP_CRITICAL,
        ], ["Q", "E"])
    ],
    Tighnari: [
        defaultRole("DPS", "西风猎弓", ["深林的记忆"], [
            FightProp.FIGHT_PROP_ATTACK_PERCENT,
            FightProp.FIGHT_PROP_GRASS_ADD_HURT,
            FightProp.FIGHT_PROP_CRITICAL,
        ], ["A", "Q", "E"])
    ],
    Dori: [
        defaultRole("SUPPORT", "西风大剑", ["绝缘之旗印"], [
            FightProp.FIGHT_PROP_CHARGE_EFFICIENCY,
            FightProp.FIGHT_PROP_HP_PERCENT,
            FightProp.FIGHT_PROP_HP_PERCENT,
        ], ["Q", "E"]),
    ],
    Nilou: [
        defaultRole("DPS", "西风剑", ["千岩牢固"], [
            FightProp.FIGHT_PROP_HP_PERCENT,
            FightProp.FIGHT_PROP_HP_PERCENT,
            FightProp.FIGHT_PROP_HP_PERCENT,
        ], ["Q", "E"]),
    ],
    Candace: [
        defaultRole("SUPPORT", "西风长枪", ["千岩牢固"], [
            FightProp.FIGHT_PROP_HP_PERCENT,
            FightProp.FIGHT_PROP_HP_PERCENT,
            FightProp.FIGHT_PROP_HP_PERCENT,
        ], ["Q", "E"]),
    ],
    Cyno: [
        defaultRole("DPS", "西风长枪", ["绝缘之旗印"], [
            FightProp.FIGHT_PROP_ATTACK_PERCENT,
            FightProp.FIGHT_PROP_ELEC_ADD_HURT,
            FightProp.FIGHT_PROP_CRITICAL,
        ], ["Q", "E"]),
    ]
};


for (const p of [Grid.Pyro, Grid.Anemo, Grid.Electro, Grid.Cryo, Grid.Hydro, Grid.Geo, Grid.Dendro]) {
    Builds = {
        ...Builds,
        ...omitBy(await fromCSV(await loadOrSync(p), p), (roles) => some(roles, (r) => r.Role.indexOf("WIP") > -1)),
    };
}