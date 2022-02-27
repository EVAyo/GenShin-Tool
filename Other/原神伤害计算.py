
from kokomi.miHoYo.Genshin import Damage


if __name__ == "__main__":
    Eula = Damage.Character(
        attack=Damage.Attack(342, 510, 0.18+0.2, 1284),
        multipiler=Damage.Multipiler(
            [1.774, 1.849, 1.123*2, 2.227, 1.42*2], 0),
        bouns=Damage.Bouns([0.25, 0.25, 0.466]),
        crit=Damage.Critical(86.6+0.08, 170.0+0.15),
        reaction=Damage.Reaction(1, 0, 0),
        defense=Damage.Defense(90, 100, 0),
        res=Damage.Resistance(0, 0.25+0.4, 0.1)
    )
    print('A:', Eula.Calcu())

    Eula.Set_Multipiler(Damage.Multipiler([4.42, 7.256, 1.482*13], 0))
    print('BF:', Eula.Calcu())
