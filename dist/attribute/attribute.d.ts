export default class Attribute {
    cureEffect: number;
    curedEffect: number;
    lifeBasic: number;
    lifeStatic: number;
    lifePercentage: number;
    attackBasic: number;
    attackStatic: number;
    attackPercentage: number;
    defendBasic: number;
    defendStatic: number;
    defendPercentage: number;
    critical: number;
    bCritical: number;
    eCritical: number;
    qCritical: number;
    airCritical: number;
    criticalDamage: number;
    thunderRes: number;
    fireRes: number;
    waterRes: number;
    iceRes: number;
    windRes: number;
    rockRes: number;
    elementalMastery: number;
    recharge: number;
    thunderBonus: number;
    fireBonus: number;
    waterBonus: number;
    iceBonus: number;
    windBonus: number;
    rockBonus: number;
    grassBonus: number;
    physicalBonus: number;
    aBonus: number;
    bBonus: number;
    eBonus: number;
    qBonus: number;
    airBonus: number;
    bonus: number;
    thunderTime: number;
    fireTime: number;
    waterTime: number;
    iceTime: number;
    windTime: number;
    rockTime: number;
    grassTime: number;
    shield: number;
    aSpeed: number;
    bSpeed: number;
    overloadEnhance: number;
    burningEnhance: number;
    electroEnhance: number;
    superconductEnhance: number;
    swirlThunderEnhance: number;
    swirlFireEnhance: number;
    swirlWaterEnhance: number;
    swirlIceEnhance: number;
    vaporizeEnhance: number;
    meltEnhance: number;
    attack(): number;
    life(): number;
    defend(): number;
    crit(value: number): void;
    elementalBonus(value: number): void;
}
