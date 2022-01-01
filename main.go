package main

import (
	"encoding/json"
	"flag"
	"log"
	"os"

	"github.com/xmdhs/genshin-card/server"
)

func main() {
	cookie := os.Getenv("COOKIE")
	if cookie == "" {
		b, err := os.ReadFile("cookie.txt")
		if err != nil {
			panic(err)
		}
		cookie = string(b)
	}
	cookies := map[string][]string{}
	err := json.Unmarshal([]byte(cookie), &cookies)
	if err != nil {
		panic(err)
	}
	log.Println(server.Server(addr, cookies))
}

var (
	addr string
)

func init() {
	flag.StringVar(&addr, "addr", "127.0.0.1:5153", "http server address")
	flag.Parse()
	if addr == "127.0.0.1:5153" && os.Getenv("PORT") != "" {
		addr = ":" + os.Getenv("PORT")
	}
}
