package server

import (
	"fmt"
	"math"
	"net/http"
	"strconv"
	"time"

	"github.com/julienschmidt/httprouter"
)

func Server(addr string, cookie map[string][]string) error {
	mux := httprouter.New()
	mux.GET("/card/:region/:server/:skin/:uid", less(cookie))
	mux.GET("/detail/:region/:server/:skin/:uid", more(cookie))

	s := http.Server{
		Addr:              addr,
		ReadHeaderTimeout: 4 * time.Second,
		WriteTimeout:      15 * time.Second,
		ReadTimeout:       7 * time.Second,
		Handler:           mux,
	}
	err := s.ListenAndServe()
	if err != nil {
		return fmt.Errorf("Server: %w", err)
	}
	return nil
}

func less(cookie map[string][]string) httprouter.Handle {
	return func(w http.ResponseWriter, r *http.Request, p httprouter.Params) {
		card, _, shouldReturn := getData(p, w, cookie)
		if shouldReturn {
			return
		}

		server := p.ByName("server")
		acard := findCardInfo(server, card)

		t := card2temp(&acard, p.ByName("skin"))

		w.Header().Set("Content-Type", "image/svg+xml")
		w.Header().Set("Cache-Control", "max-age=600")
		w.Write([]byte(t.Parse()))
	}
}

func more(cookie map[string][]string) httprouter.Handle {
	return func(w http.ResponseWriter, r *http.Request, p httprouter.Params) {
		card, c, shouldReturn := getData(p, w, cookie)
		if shouldReturn {
			return
		}
		server := p.ByName("server")
		acard := findCardInfo(server, card)

		gameUid, err := strconv.Atoi(acard.GameRoleID)
		if err != nil {
			httpErrf(w, "invalid uid", 1, http.StatusBadRequest)
			return
		}
		d, err := c.GetRoleIndex(gameUid, server)
		if err != nil {
			httpErrf(w, err.Error(), -1, 500)
			return
		}

		t := card2temp(&acard, p.ByName("skin"))
		t.More = true
		t.C1 = getForMap(d.Data.Stats, "luxurious_chest_number")
		t.C2 = getForMap(d.Data.Stats, "precious_chest_number")
		t.C3 = getForMap(d.Data.Stats, "exquisite_chest_number")
		t.C4 = getForMap(d.Data.Stats, "common_chest_number")

		all := 0
		for _, v := range d.Data.WorldExplorations {
			all += v.ExplorationPercentage
		}
		fall := float64(all) / float64(len(d.Data.WorldExplorations))
		fall = math.Trunc(fall+0.5) / 10
		t.World = fmt.Sprintf("%v%%", fall)

		w.Header().Set("Content-Type", "image/svg+xml")
		w.Header().Set("Cache-Control", "max-age=1200")
		w.Write([]byte(t.Parse()))
	}
}
