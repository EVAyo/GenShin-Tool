package api

import (
	"crypto/md5"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"math/rand"
	"net/http"
	"net/url"
	"strconv"
	"time"
)

var arand = rand.New(rand.NewSource(time.Now().UnixNano()))

func randStr(i int) string {
	s := "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	b := make([]byte, i)
	for i := range b {
		b[i] = s[arand.Intn(len(s))]
	}
	return string(b)
}

var MihoyoAPI = map[string]ApiConfig{
	"hoyolab": {
		FetchRoleIDURL:      "https://bbs-api-os.mihoyo.com/game_record/card/wapi/getGameRecordCard",
		FetchRoleIndexURL:   "https://bbs-api-os.mihoyo.com/game_record/genshin/api/index",
		FetchSpiralAbyssURL: "https://bbs-api-os.mihoyo.com/game_record/genshin/api/spiralAbyss",
		Cookie:              "",
		GetDs: func(_ ...string) string {
			key := "6s25p5ox5y14umn1p61aqyyvbvvl3lrt"
			nowtime := time.Now().Unix()
			r := randStr(6)
			s := fmt.Sprintf("salt=%v&t=%v&r=%v", key, nowtime, r)
			m := md5.New()
			m.Write([]byte(s))
			md5s := hex.EncodeToString(m.Sum(nil))
			return fmt.Sprintf("%v,%v,%v", nowtime, r, md5s)
		},
		Referer:        "https://webstatic-sea.mihoyo.com/",
		XRpcAppVersion: "1.5.0",
		XRpClientType:  "5",
		Client:         http.Client{Timeout: 10 * time.Second},
		UseCache:       true,
		UserAgent:      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
	},
}

type ApiConfig struct {
	FetchRoleIDURL      string
	FetchRoleIndexURL   string
	FetchSpiralAbyssURL string
	Cookie              string
	GetDs               func(s ...string) string
	Referer             string
	XRpcAppVersion      string
	XRpClientType       string
	Client              http.Client
	UseCache            bool
	UserAgent           string
}

func (a *ApiConfig) httpGet(url string) ([]byte, error) {
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return nil, fmt.Errorf("httpGet: %w", err)
	}
	req.Header.Set("Cookie", a.Cookie)
	req.Header.Set("Referer", a.Referer)
	req.Header.Set("x-rpc-app_version", a.XRpcAppVersion)
	req.Header.Set("x-rpc-client_type", a.XRpClientType)
	req.Header.Set("x-rpc-language", "zh-cn")
	req.Header.Set("User-Agent", a.UserAgent)
	req.Header.Set("DS", a.GetDs())
	resp, err := a.Client.Do(req)
	if resp != nil {
		defer resp.Body.Close()
	}
	if err != nil {
		return nil, fmt.Errorf("httpGet: %w", err)
	}
	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("httpGet: %w", HttpErr{code: resp.StatusCode})
	}
	b, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("httpGet: %w", err)
	}
	return b, nil
}

func (a *ApiConfig) GetRoleInfo(uid int) (*Card, error) {
	u, err := url.Parse(a.FetchRoleIDURL)
	if err != nil {
		return nil, fmt.Errorf("GetRoleInfo: %w", err)
	}
	q := u.Query()
	q.Set("uid", strconv.Itoa(uid))
	u.RawQuery = q.Encode()

	b, err := a.getSome(u.String(), time.Hour*6)
	if err != nil {
		return nil, fmt.Errorf("GetRoleInfo: %w", err)
	}
	var c Card
	if err := json.Unmarshal(b, &c); err != nil {
		return nil, fmt.Errorf("GetRoleInfo: %w", err)
	}
	return &c, nil
}

func (a *ApiConfig) getSome(url string, expTime time.Duration) ([]byte, error) {
	var b []byte
	if a.UseCache {
		b = acache.Load(url)
	}

	if b == nil {
		var err error
		b, err = a.httpGet(url)
		if err != nil {
			return nil, fmt.Errorf("getSome: %w", err)
		}
		if a.UseCache {
			acache.Store(url, b, time.Now().Add(expTime))
		}
	}
	return b, nil
}

func (a *ApiConfig) GetRoleIndex(gameId int, region string) (*Detail, error) {
	u, err := url.Parse(a.FetchRoleIndexURL)
	if err != nil {
		return nil, fmt.Errorf("GetRoleIndex: %w", err)
	}
	q := u.Query()
	q.Set("role_id", strconv.Itoa(gameId))
	q.Set("server", region)
	u.RawQuery = q.Encode()

	b, err := a.getSome(u.String(), 48*time.Hour)
	if err != nil {
		return nil, fmt.Errorf("GetRoleIndex: %w", err)
	}
	var r Detail
	if err := json.Unmarshal(b, &r); err != nil {
		return nil, fmt.Errorf("GetRoleIndex: %w", err)
	}
	return &r, nil
}

func (a *ApiConfig) GetSpiralAbyss(gameId int, region string) (*Abyss, error) {
	u, err := url.Parse(a.FetchSpiralAbyssURL)
	if err != nil {
		return nil, fmt.Errorf("GetRoleIndex: %w", err)
	}
	q := url.Values{}
	q.Set("role_id", strconv.Itoa(gameId))
	q.Set("server", region)
	q.Set("schedule_type", "1")
	u.RawQuery = q.Encode()

	b, err := a.getSome(u.String(), 48*time.Hour)
	if err != nil {
		return nil, fmt.Errorf("GetRoleIndex: %w", err)
	}
	var r Abyss
	if err := json.Unmarshal(b, &r); err != nil {
		return nil, fmt.Errorf("GetRoleIndex: %w", err)
	}
	return &r, nil
}

type HttpErr struct {
	code int
}

func (e HttpErr) Error() string {
	return fmt.Sprintf("http error: %d", e.code)
}
