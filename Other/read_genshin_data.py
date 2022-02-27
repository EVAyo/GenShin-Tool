
import pylab as lab
from kokomi.miHoYo.Genshin import ConfigData
import itertools


def make_weapon_level_curve():
    data = ConfigData.Weapon.LevelExcel()
    s1 = sum(data['White'])
    s2 = sum(data['Green'])
    s3 = sum(data['Blue'])
    s4 = sum(data['Purple'])
    s5 = sum(data['Golden'])

    x = [i for i in range(0, 90)]
    lab.plot(x, list(itertools.accumulate(data['White'])), color='black')
    lab.plot(x, list(itertools.accumulate(data['Green'])), color='green')
    lab.plot(x, list(itertools.accumulate(data['Blue'])), color='blue')
    lab.plot(x, list(itertools.accumulate(data['Purple'])), color='purple')
    lab.plot(x, list(itertools.accumulate(data['Golden'])), color='yellow')
    # lab.show()
    lab.gcf().set_size_inches(27, 35)
    lab.savefig('weapon_level_exp_1.png')


if __name__ == '__main__':
    ConfigData.Weapon.AllWeapon()
