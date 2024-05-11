package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"strconv"

	"github.com/go-redis/redis/v8"
	"github.com/sirupsen/logrus"
)

var rdb *redis.Client

func init() {
	logrus.SetFormatter(&logrus.JSONFormatter{})
	logrus.Info("Logger initialized")
	logrus.SetLevel(logrus.InfoLevel)

	opt, err := redis.ParseURL(os.Getenv("REDIS_URL"))
	if err != nil {
		panic(err)
	}
	rdb = redis.NewClient(opt)
}

func main() {
	debug := os.Getenv("DEBUG")
	if debug == "1" {
		logrus.SetLevel(logrus.DebugLevel)
		logrus.Debug("Logging debug output, run without DEBUG=1 to disable")
	}

	port := os.Getenv("PORT")
	if port == "" {
		logrus.Fatal("PORT environment variable is not set")
	}

	http.HandleFunc("GET /coords/{x1}/{y1}/", HandleCoords)
	logrus.Infof("Listening on port %s", port)
	if err := http.ListenAndServe(fmt.Sprintf(":%s", port), nil); err != nil {
		logrus.Error("Failure in running coords server")
	}
}

type CoordsResponse struct {
	X     int    `json:"x"`
	Y     int    `json:"y"`
	Color string `json:"color"`
	Draw  bool   `json:"draw"`
}

type CoordsRedis struct {
	X     int    `redis:"x"`
	Y     int    `redis:"y"`
	Color string `redis:"color"`
	Draw  bool   `redis:"draw"`
}

func HandleCoords(w http.ResponseWriter, r *http.Request) {
	log := logrus.WithFields(logrus.Fields{"endpoint": "HandleCoords"})
	ctx := r.Context()

	x1, _ := strconv.Atoi(r.PathValue("x1"))
	y1, _ := strconv.Atoi(r.PathValue("y1"))

	w.Header().Set("Access-Control-Allow-Origin", "*")

	var responses []CoordsResponse

	for y := 0; y < y1; y++ {
		for x := 0; x < x1; x++ {
			key := "coords:" + strconv.Itoa(y) + ":" + strconv.Itoa(x)
			res := rdb.HGetAll(ctx, key)
			if err := res.Err(); err != nil {
				http.Error(w, "Error fetching from redis:"+err.Error(), http.StatusInternalServerError)
				return
			}
			var hmap CoordsRedis
			if err := res.Scan(&hmap); err != nil {
				panic(err)
			}
			if hmap.Color == "" {
				continue
			}

			responses = append(responses,
				CoordsResponse{
					X:     hmap.X,
					Y:     hmap.Y,
					Color: hmap.Color,
					Draw:  hmap.Draw,
				})
			log.Debugf("found something y=%d x=%d", hmap.Y, hmap.X)
		}
	}

	w.Header().Set("Content-Type", "application/json")

	json.NewEncoder(w).Encode(map[string][]CoordsResponse{"coords": responses})
}
