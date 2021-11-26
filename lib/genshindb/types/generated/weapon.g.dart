// GENERATED CODE - DO NOT MODIFY BY HAND

part of '../weapon.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$_Weapon _$$_WeaponFromJson(Map<String, dynamic> json) => _$_Weapon(
      id: json['Id'] as int,
      name: I18n.fromJson(json['Name'] as Map<String, dynamic>),
      desc: I18n.fromJson(json['Desc'] as Map<String, dynamic>),
      rarity: json['Rarity'] as int,
      weaponType: $enumDecode(_$WeaponTypeEnumMap, json['WeaponType']),
      affixes: (json['Affixes'] as List<dynamic>)
          .map((e) => (e as List<dynamic>)
              .map((e) => EquipAffix.fromJson(e as Map<String, dynamic>))
              .toList())
          .toList(),
      promoteId: json['PromoteId'] as int,
      propGrowCurveAndInitials:
          (json['PropGrowCurveAndInitials'] as Map<String, dynamic>).map(
        (k, e) => MapEntry($enumDecode(_$FightPropEnumMap, k),
            PropGrowCurveAndInitial.fromJson(e as Map<String, dynamic>)),
      ),
    );

Map<String, dynamic> _$$_WeaponToJson(_$_Weapon instance) => <String, dynamic>{
      'Id': instance.id,
      'Name': instance.name,
      'Desc': instance.desc,
      'Rarity': instance.rarity,
      'WeaponType': _$WeaponTypeEnumMap[instance.weaponType],
      'Affixes': instance.affixes,
      'PromoteId': instance.promoteId,
      'PropGrowCurveAndInitials': instance.propGrowCurveAndInitials
          .map((k, e) => MapEntry(_$FightPropEnumMap[k], e)),
    };

const _$WeaponTypeEnumMap = {
  WeaponType.SWORD_ONE_HAND: 'WEAPON_SWORD_ONE_HAND',
  WeaponType.WEAPON_CLAYMORE: 'WEAPON_CLAYMORE',
  WeaponType.WEAPON_POLE: 'WEAPON_POLE',
  WeaponType.POLE: 'WEAPON_BOW',
  WeaponType.CATALYST: 'WEAPON_CATALYST',
};

const _$FightPropEnumMap = {
  FightProp.LEVEL: 'FIGHT_PROP_LEVEL',
  FightProp.ENEMY_ADD_LEVEL: 'FIGHT_PROP_ENEMY_ADD_LEVEL',
  FightProp.ADD_LEVEL: 'FIGHT_PROP_ADD_LEVEL',
  FightProp.ADD_ELEMENTAL_SKILL_LEVEL: 'FIGHT_PROP_ADD_ELEMENTAL_SKILL_LEVEL',
  FightProp.ADD_ELEMENTAL_BURST_LEVEL: 'FIGHT_PROP_ADD_ELEMENTAL_BURST_LEVEL',
  FightProp.BASE_HP: 'FIGHT_PROP_BASE_HP',
  FightProp.BASE_ATTACK: 'FIGHT_PROP_BASE_ATTACK',
  FightProp.BASE_DEFENSE: 'FIGHT_PROP_BASE_DEFENSE',
  FightProp.HP: 'FIGHT_PROP_HP',
  FightProp.HP_PERCENT: 'FIGHT_PROP_HP_PERCENT',
  FightProp.ATTACK: 'FIGHT_PROP_ATTACK',
  FightProp.ATTACK_PERCENT: 'FIGHT_PROP_ATTACK_PERCENT',
  FightProp.DEFENSE: 'FIGHT_PROP_DEFENSE',
  FightProp.DEFENSE_PERCENT: 'FIGHT_PROP_DEFENSE_PERCENT',
  FightProp.CRITICAL: 'FIGHT_PROP_CRITICAL',
  FightProp.CRITICAL_HURT: 'FIGHT_PROP_CRITICAL_HURT',
  FightProp.CHARGE_EFFICIENCY: 'FIGHT_PROP_CHARGE_EFFICIENCY',
  FightProp.HEAL_ADD: 'FIGHT_PROP_HEAL_ADD',
  FightProp.HEALED_ADD: 'FIGHT_PROP_HEALED_ADD',
  FightProp.ELEMENT_MASTERY: 'FIGHT_PROP_ELEMENT_MASTERY',
  FightProp.FIRE_ADD_HURT: 'FIGHT_PROP_FIRE_ADD_HURT',
  FightProp.ELEC_ADD_HURT: 'FIGHT_PROP_ELEC_ADD_HURT',
  FightProp.WATER_ADD_HURT: 'FIGHT_PROP_WATER_ADD_HURT',
  FightProp.WIND_ADD_HURT: 'FIGHT_PROP_WIND_ADD_HURT',
  FightProp.ROCK_ADD_HURT: 'FIGHT_PROP_ROCK_ADD_HURT',
  FightProp.GRASS_ADD_HURT: 'FIGHT_PROP_GRASS_ADD_HURT',
  FightProp.ICE_ADD_HURT: 'FIGHT_PROP_ICE_ADD_HURT',
  FightProp.PHYSICAL_ADD_HURT: 'FIGHT_PROP_PHYSICAL_ADD_HURT',
  FightProp.FIRE_SUB_HURT: 'FIGHT_PROP_FIRE_SUB_HURT',
  FightProp.ELEC_SUB_HURT: 'FIGHT_PROP_ELEC_SUB_HURT',
  FightProp.WATER_SUB_HURT: 'FIGHT_PROP_WATER_SUB_HURT',
  FightProp.WIND_SUB_HURT: 'FIGHT_PROP_WIND_SUB_HURT',
  FightProp.ROCK_SUB_HURT: 'FIGHT_PROP_ROCK_SUB_HURT',
  FightProp.GRASS_SUB_HURT: 'FIGHT_PROP_GRASS_SUB_HURT',
  FightProp.ICE_SUB_HURT: 'FIGHT_PROP_ICE_SUB_HURT',
  FightProp.PHYSICAL_SUB_HURT: 'FIGHT_PROP_PHYSICAL_SUB_HURT',
  FightProp.ADD_HURT: 'FIGHT_PROP_ADD_HURT',
  FightProp.SUB_HURT: 'FIGHT_PROP_SUB_HURT',
  FightProp.NORMAL_ATTACK_ADD_HURT: 'FIGHT_PROP_NORMAL_ATTACK_ADD_HURT',
  FightProp.NORMAL_ATTACK_ADD_CRITICAL: 'FIGHT_PROP_NORMAL_ATTACK_ADD_CRITICAL',
  FightProp.CHARGED_ATTACK_ADD_HURT: 'FIGHT_PROP_CHARGED_ATTACK_ADD_HURT',
  FightProp.CHARGED_ATTACK_ADD_CRITICAL:
      'FIGHT_PROP_CHARGED_ATTACK_ADD_CRITICAL',
  FightProp.PLUNGING_ATTACK_ADD_HURT: 'FIGHT_PROP_PLUNGING_ATTACK_ADD_HURT',
  FightProp.PLUNGING_ATTACK_ADD_CRITICAL:
      'FIGHT_PROP_PLUNGING_ATTACK_ADD_CRITICAL',
  FightProp.ELEMENTAL_SKILL_ADD_HURT: 'FIGHT_PROP_ELEMENTAL_SKILL_ADD_HURT',
  FightProp.ELEMENTAL_SKILL_ADD_CRITICAL:
      'FIGHT_PROP_ELEMENTAL_SKILL_ADD_CRITICAL',
  FightProp.ELEMENTAL_BURST_ADD_HURT: 'FIGHT_PROP_ELEMENTAL_BURST_ADD_HURT',
  FightProp.ELEMENTAL_BURST_ADD_CRITICAL:
      'FIGHT_PROP_ELEMENTAL_BURST_ADD_CRITICAL',
  FightProp.MELT_ADD_HURT: 'FIGHT_PROP_MELT_ADD_HURT',
  FightProp.VAPORIZE_ADD_HURT: 'FIGHT_PROP_VAPORIZE_ADD_HURT',
  FightProp.SUPER_CONDUCT_ADD_HURT: 'FIGHT_PROP_SUPER_CONDUCT_ADD_HURT',
  FightProp.SWIRL_ADD_HURT: 'FIGHT_PROP_SWIRL_ADD_HURT',
  FightProp.ELECTRO_CHARGED_ADD_HURT: 'FIGHT_PROP_ELECTRO_CHARGED_ADD_HURT',
  FightProp.OVERLOADED_ADD_HURT: 'FIGHT_PROP_OVERLOADED_ADD_HURT',
  FightProp.SHATTERED_ADD_HURT: 'FIGHT_PROP_SHATTERED_ADD_HURT',
  FightProp.SHIELD_COST_MINUS_RATIO: 'FIGHT_PROP_SHIELD_COST_MINUS_RATIO',
  FightProp.ENEMY_LEVEL: 'FIGHT_PROP_ENEMY_LEVEL',
  FightProp.ENEMY_RESISTANCE: 'FIGHT_PROP_ENEMY_RESISTANCE',
  FightProp.ENEMY_SUB_RESISTANCE: 'FIGHT_PROP_ENEMY_SUB_RESISTANCE',
  FightProp.ENEMY_SUB_DEFENSE: 'FIGHT_PROP_ENEMY_SUB_DEFENSE',
  FightProp.SPEED_PERCENT: 'FIGHT_PROP_SPEED_PERCENT',
  FightProp.SKILL_CD_MINUS_RATIO: 'FIGHT_PROP_SKILL_CD_MINUS_RATIO',
  FightProp.ATTACK_ADD_RADIO: 'FIGHT_PROP_ATTACK_ADD_RADIO',
  FightProp.ELEMENTAL_BURST_ADD_HURT_ON_CHARGE_EFFICIENCY:
      'FIGHT_PROP_ELEMENTAL_BURST_ADD_HURT_ON_CHARGE_EFFICIENCY',
  FightProp.ATTACK_PERCENT_ON_CHARGE_EFFICIENCY:
      'FIGHT_PROP_ATTACK_PERCENT_ON_CHARGE_EFFICIENCY',
  FightProp.ATTACK_PERCENT_ON_HP: 'FIGHT_PROP_ATTACK_PERCENT_ON_HP',
};
