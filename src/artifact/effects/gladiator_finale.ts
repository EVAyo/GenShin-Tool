import Attribute from "../../attribute/attribute"
import Param from "../param";

function apply2(attribute: Attribute, params: Param) {
    attribute.attackPercentage += attribute.attackBasic * 0.18;
}

function apply4(attribute: Attribute, params: Param) {
    if (params.countGladiatorFinale) {
        attribute.aBonus += 0.35;
    }
}

export default [null, apply2, null, apply4, null];