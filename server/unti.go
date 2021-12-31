package server

import (
	"embed"
	"encoding/base64"
	"encoding/json"
	"log"
	"math/rand"
	"net/http"
	"strconv"
	"time"

	"github.com/julienschmidt/httprouter"
	"github.com/xmdhs/genshin-card/api"
	"github.com/xmdhs/genshin-card/template"
)

type httpErr struct {
	Code int    `json:"code"`
	Msg  string `json:"msg"`
}

func httpErrf(w http.ResponseWriter, err string, code, httpCode int) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(httpCode)
	e := httpErr{
		Code: code,
		Msg:  err,
	}
	if err := json.NewEncoder(w).Encode(e); err != nil {
		panic(err)
	}
	log.Println(e)
}

//go:embed imgs
var imgs embed.FS

var arand = rand.New(rand.NewSource(time.Now().UnixNano()))

func getSkin(skin string) string {
	if skin == "rand" {
		i := arand.Intn(40)
		skin = strconv.Itoa(i)
	}
	b, err := imgs.ReadFile("imgs/" + skin + ".jpg")
	if err != nil {
		return ""
	}
	return "data:image/jpeg;base64," + base64.StdEncoding.EncodeToString(b)
}

func card2temp(c *api.CardDataList, skin string) template.Card {
	tc := template.Card{
		More:       false,
		SkinBase64: getSkin(skin),
		Name:       c.Nickname,
		Level:      c.Level,
		UID: func() int {
			i, _ := strconv.Atoi(c.GameRoleID)
			return i
		}(),
	}

	for _, v := range c.Data {
		switch v.Name {
		case "活跃天数":
			tc.ActiveDays, _ = strconv.Atoi(v.Value)
		case "获得角色数":
			tc.Avatar, _ = strconv.Atoi(v.Value)
		case "成就达成数":
			tc.Achievement, _ = strconv.Atoi(v.Value)
		case "深境螺旋":
			tc.Wpiral = v.Value
		}
	}

	return tc
}

func findCardInfo(server string, card *api.Card) api.CardDataList {
	acard := api.CardDataList{}
	for _, v := range card.Data.List {
		if v.Region == server {
			acard = v
			break
		}
	}
	return acard
}

func getData(p httprouter.Params, w http.ResponseWriter, cookies []string) (*api.Card, *api.ApiConfig, bool) {
	c, ok := api.MihoyoAPI[p.ByName("region")]
	if !ok {
		httpErrf(w, "region not found", 1, http.StatusBadRequest)
		return nil, nil, true
	}
	cookie := cookies[arand.Intn(len(cookies))]
	c.Cookie = cookie

	uid, err := strconv.Atoi(p.ByName("uid"))
	if err != nil {
		httpErrf(w, "uid not found", 2, http.StatusBadRequest)
		return nil, nil, true
	}
	card, err := c.GetRoleInfo(uid)
	if err != nil {
		httpErrf(w, err.Error(), -1, 500)
		return nil, nil, true
	}
	if card.Retcode != 0 {
		http.Error(w, card.Message, 500)
		return nil, nil, true
	}
	return card, &c, false
}

func getForMap(m map[string]interface{}, key string) int {
	v, ok := m[key]
	if !ok {
		return 0
	}
	return int(v.(float64))
}
