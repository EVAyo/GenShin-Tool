package template

import (
	"bytes"
	_ "embed"
	"text/template"
)

//go:embed 1.svg
var svg []byte

var t *template.Template

func init() {
	var err error
	t = template.New("svg")
	t, err = t.Parse(string(svg))
	if err != nil {
		panic(err)
	}
}

type Card struct {
	More        bool
	SkinBase64  string
	Name        string
	Level       int
	UID         int
	C1          int
	C2          int
	C3          int
	C4          int
	ActiveDays  int
	Avatar      int
	Achievement int
	Wpiral      string
	World       string
}

func (c Card) Parse() string {
	w := &bytes.Buffer{}
	t.ExecuteTemplate(w, "svg", c)
	return w.String()
}
