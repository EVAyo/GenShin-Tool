import { Attribute } from "./attribute";
import {
    getCharacterAttribute, getWeaponAttribute,
    applyCharacterBase, applyWeaponBase,
    applyCharacterSecondary, applyWeaponSecondary
} from "./numeric";
import { newAttribute } from "./attribute";
// import { mixAttribute, capitalize } from "./util/util";
import { apply as applyArtifacts, Param, IArtifact, ArtifactType, ArtifactSet } from "./artifact";
import { TagName } from "./artifact/tag_type";

// 角色与武器数据
export {
    getCharacterAttribute, getWeaponAttribute
    // applyCharacterBase, applyWeaponBase,
    // applyCharacterSecondary, applyWeaponSecondary
} from "./numeric";

// 圣遗物
export { apply as applyArtifacts } from "./artifact";

// 属性
export { newAttribute } from "./attribute";


// function createArtifact(obj: IArtifact): Artifact | null {
//     try {
//         let art = new Artifact(obj.position, obj.setName);
//         art.setPrimaryTag(obj.primary.tag, obj.primary.value);
//         for (let i = 0; i < obj.secondary.length; i++) {
//             let temp = obj.secondary[i];
//             art.addSecondaryTag(temp.tag, temp.value);
//         }
    
//         return art;
//     } catch (err) {
//         return null;
//     }
// }

export function compose(character: string, weapon: string, artifacts?: IArtifact[], params?: Param): Attribute | null {
    let base = newAttribute();

    let a1 = getCharacterAttribute(character);
    if (a1 === null) {
        return null;
    }

    let a2 = getWeaponAttribute(weapon);
    if (a2 === null) {
        return null;
    }
    
    applyCharacterBase(base, a1);
    applyWeaponBase(base, a2);
    applyCharacterSecondary(base, a1);
    applyWeaponSecondary(base, a2);

    if (!artifacts || artifacts.length === 0) {
        return base;
    }

    params = params || {};
    applyArtifacts(base, artifacts, params);
    
    return base;
}

// export function compose(character: string, weapon: string, artifacts: Artifact[], params?: Param): Attribute | null {
//     let base: Attribute | null = composeBasic(character, weapon);
//     if (base === null) {
//         return null;
//     }

//     params = params || {};

//     applyArtifacts(base, artifacts, params);

//     return base;
// }