package template

import (
	_ "embed"
	"fmt"
	"testing"
)

func TestCard_Parse(t *testing.T) {
	c := Card{
		More:        true,
		SkinBase64:  "",
		Name:        "nil",
		Level:       0,
		UID:         0,
		C1:          0,
		C2:          0,
		C3:          0,
		C4:          0,
		ActiveDays:  0,
		Avatar:      0,
		Achievement: 0,
		Wpiral:      "12-33",
		World:       "200%",
	}
	fmt.Println(c.Parse())
}
