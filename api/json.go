package api

type Card struct {
	Data    cardData `json:"data"`
	Message string   `json:"message"`
	Retcode int      `json:"retcode"`
}

type cardData struct {
	List []CardDataList `json:"list"`
}

type CardDataList struct {
	BackgroundImage string                   `json:"background_image"`
	Data            []cardDataListDatum      `json:"data"`
	DataSwitches    []cardDataListDataSwitch `json:"data_switches"`
	GameID          int                      `json:"game_id"`
	GameRoleID      string                   `json:"game_role_id"`
	H5DataSwitches  []interface{}            `json:"h5_data_switches"`
	HasRole         bool                     `json:"has_role"`
	IsPublic        bool                     `json:"is_public"`
	Level           int                      `json:"level"`
	Nickname        string                   `json:"nickname"`
	Region          string                   `json:"region"`
	RegionName      string                   `json:"region_name"`
	URL             string                   `json:"url"`
}

type cardDataListDatum struct {
	Name  string `json:"name"`
	Type  int    `json:"type"`
	Value string `json:"value"`
}

type cardDataListDataSwitch struct {
	IsPublic   bool   `json:"is_public"`
	SwitchID   int    `json:"switch_id"`
	SwitchName string `json:"switch_name"`
}

type Detail struct {
	Data    detailData `json:"data"`
	Message string     `json:"message"`
	Retcode int        `json:"retcode"`
}

type detailData struct {
	Avatars           []detailDataAvatar           `json:"avatars"`
	CityExplorations  []interface{}                `json:"city_explorations"`
	Homes             []detailDataHome             `json:"homes"`
	Role              interface{}                  `json:"role"`
	Stats             map[string]interface{}       `json:"stats"`
	WorldExplorations []detailDataWorldExploration `json:"world_explorations"`
}

type detailDataAvatar struct {
	ActivedConstellationNum int    `json:"actived_constellation_num"`
	Element                 string `json:"element"`
	Fetter                  int    `json:"fetter"`
	ID                      int    `json:"id"`
	Image                   string `json:"image"`
	Level                   int    `json:"level"`
	Name                    string `json:"name"`
	Rarity                  int    `json:"rarity"`
}

type detailDataHome struct {
	ComfortLevelIcon string `json:"comfort_level_icon"`
	ComfortLevelName string `json:"comfort_level_name"`
	ComfortNum       int    `json:"comfort_num"`
	Icon             string `json:"icon"`
	ItemNum          int    `json:"item_num"`
	Level            int    `json:"level"`
	Name             string `json:"name"`
	VisitNum         int    `json:"visit_num"`
}

type detailDataWorldExploration struct {
	ExplorationPercentage int                                  `json:"exploration_percentage"`
	Icon                  string                               `json:"icon"`
	ID                    int                                  `json:"id"`
	Level                 int                                  `json:"level"`
	Name                  string                               `json:"name"`
	Offerings             []detailDataWorldExplorationOffering `json:"offerings"`
	Type                  string                               `json:"type"`
}

type detailDataWorldExplorationOffering struct {
	Level int    `json:"level"`
	Name  string `json:"name"`
}

type Abyss struct {
	Data    abyssData `json:"data"`
	Message string    `json:"message"`
	Retcode int       `json:"retcode"`
}

type abyssData struct {
	DamageRank       []abyssRank      `json:"damage_rank"`
	DefeatRank       []abyssRank      `json:"defeat_rank"`
	EndTime          string           `json:"end_time"`
	EnergySkillRank  []abyssRank      `json:"energy_skill_rank"`
	Floors           []abyssDataFloor `json:"floors"`
	IsUnlock         bool             `json:"is_unlock"`
	MaxFloor         string           `json:"max_floor"`
	NormalSkillRank  []abyssRank      `json:"normal_skill_rank"`
	RevealRank       []abyssRank      `json:"reveal_rank"`
	ScheduleID       int              `json:"schedule_id"`
	StartTime        string           `json:"start_time"`
	TakeDamageRank   []abyssRank      `json:"take_damage_rank"`
	TotalBattleTimes int              `json:"total_battle_times"`
	TotalStar        int              `json:"total_star"`
	TotalWinTimes    int              `json:"total_win_times"`
}

type abyssDataFloor struct {
	Icon       string                `json:"icon"`
	Index      int                   `json:"index"`
	IsUnlock   bool                  `json:"is_unlock"`
	Levels     []abyssDataFloorLevel `json:"levels"`
	MaxStar    int                   `json:"max_star"`
	SettleTime string                `json:"settle_time"`
	Star       int                   `json:"star"`
}

type abyssDataFloorLevel struct {
	Battles []abyssDataFloorLevelBattle `json:"battles"`
	Index   int                         `json:"index"`
	MaxStar int                         `json:"max_star"`
	Star    int                         `json:"star"`
}

type abyssDataFloorLevelBattle struct {
	Avatars   []abyssDataFloorLevelBattleAvatar `json:"avatars"`
	Index     int                               `json:"index"`
	Timestamp string                            `json:"timestamp"`
}

type abyssDataFloorLevelBattleAvatar struct {
	Icon   string `json:"icon"`
	ID     int    `json:"id"`
	Level  int    `json:"level"`
	Rarity int    `json:"rarity"`
}

type abyssRank struct {
	AvatarIcon string `json:"avatar_icon"`
	AvatarID   int    `json:"avatar_id"`
	Rarity     int    `json:"rarity"`
	Value      int    `json:"value"`
}
