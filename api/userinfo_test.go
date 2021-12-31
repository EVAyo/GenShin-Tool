package api

import (
	"encoding/json"
	"testing"

	"fmt"
)

func TestApiConfig_GetRoleInfo(t *testing.T) {
	c := MihoyoAPI["hoyolab"]
	c.Cookie = "mi18nLang=zh-cn; _ga_YPZHJ46G8M=GS1.1.1613814072.2.1.1613814248.0; _MHYUUID=8cd045f6-a6c5-4214-89d7-aed716153102; _ga_C7LP62SPC3=GS1.1.1615977661.2.1.1615977732.0; _ga_T29RZCYXZ9=GS1.1.1619446770.6.1.1619447169.0; _ga_B5FWNDKKP0=GS1.1.1619579607.1.1.1619579647.0; _ga=GA1.1.973544679.1613718144; _ga_88EC1VG6YY=GS1.1.1624762891.2.1.1624763179.0; ltoken=8u95BKxc76WiJzRmZ4O2L2jwZPpGhWoMGM4a3rZw; ltuid=190786468; cookie_token=xO5yH8ls98RKiXzEvQCtSG8IxgE2Od4DimNiFFse; account_id=190786468"
	cc, err := c.GetRoleInfo(93586069)
	if err != nil {
		t.Error(err)
	}
	s, _ := json.Marshal(cc)
	fmt.Println(string(s))
}
