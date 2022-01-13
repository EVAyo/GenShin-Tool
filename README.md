# Artifact-master

## 前言

做出这个系统的起因其实说起来很简单，就是作为一个选择困难星人每天面对着几千个圣遗物做选择简直太太太太痛苦了。再者原神这个游戏开服一年多了对于圣遗物的评判标准很多，但一直都没有一个统一的体系，有的只能评价强化后的圣遗物。我作为一个学数据的学生想着能不能做这样一个评价体系，能够以一个统一的标准评价所有的圣遗物，以解决大家（尤其是我自己）选择圣遗物的痛苦。

在跟萌新朋友的交流过程中她跟我讲口算会更方便，我看着她50个圣遗物的背包陷入了沉思。所以该系统主要适用于和我一样角色类型比较齐全（有生命防御依赖的角色，会纠结生命防御圣遗物好不好），以及圣遗物背包爆炸（装不下，怎么想圣遗物都装不下）的玩家。

事先说明这个评价标准是基于我开服以来的游戏经验，以及诸多大佬的统计数据研究的基础上得来的，有非常多的误差与局限性，仅作抛砖引玉，欢迎各位提出意见与建议，我们一起去完善这个评价体系。这个系统我也打磨了几个月，目前来说自己使用没有遇到太多的问题，在年前发出来也是作为一个给大家也是给我自己的一个新年礼物，大家新年快乐！

## 使用说明

先上网页链接：[https://tseflcz.github.io/artifacts-master/](https://tseflcz.github.io/artifacts-master/)

我在github上发布了一个静态网页，可以批量导入圣遗物，可以配合[Amenoma](http://g.nga.cn/read.php?tid=28172053)、[Yas](https://bbs.nga.cn/read.php?tid=28834013)、[Cocogoat](https://bbs.nga.cn/read.php?tid=26328712)等圣遗物扫描工具食用。目前仅支持莫纳占卜铺格式的json文件，并且由于四星与五星的圣遗物在计算期望时有很大区别，目前仅支持五星圣遗物的计算（因为没什么人用四星圣遗物，当然主要是懒）。

不同副词条的权重可以自行设置，这里引入了主属性权重以及攻击-生命（防御）转化率的概念。主属性权重即为主属性的评分占整个评分的比例，这个权重越大主属性比副词条越重要。攻击-生命（防御）转化率是对生命（防御）角色而言，一条攻击词条相当于多少条生命防御词条，如荒泷一斗一个攻击词条大约相当于0.5个防御词条，这里转化率就设为0.5，此时攻击词条将乘0.5后算入词条数，更详细的内容可以到评分公式部分进一步了解。

这里默认设置的权重是我自己使用的供大家参考。一个小攻击对大多数角色来说相当于0.5个大攻击故权重设置为0.5，小防御小生命同理。暴击爆伤设为1.2是因为圣遗物强化时有四档，这里取所有属性的最高档为一个词条，又因为暴击爆伤比较珍贵，所以改用平均档为一个词条，1/0.85=1.17，故这里近似取1.2。

筛选功能可以按需要筛选圣遗物的套装、部位、主词条、等级，并可根据圣遗物评分、期望词条数以及当前词条数排序。圣遗物评分为主属性评分加上期望词条数，其中期望词条数为圣遗物强化到满级时期望的有效副词条数，如果希望只考虑副词条而不考虑主属性可以直接使用期望词条数对圣遗物进行评价，更详细的内容可以到评分公式部分进一步了解。

注意事项：1.由于三词条圣遗物词条数过少，在计算期望时将不会判断该词条是否有效，并且期望仅反应圣遗物强化时的可能结果，在等级较高时会有更准确的评价效果，如果有条件建议将期望不错的胚子强化以后再做判断。2.主词条评价时引入属性使用率作为评判标准，本质上是用现有角色的需求状况预测以后出的角色总体需求状况，但事实上新出的角色更多的会区别于老角色的定位，对未来可期的圣遗物评价有限，所以主词条评分还请酌情参考。

特别鸣谢：ideles大佬的网页模板与授权，[圣遗物强化助手原帖地址](https://bbs.nga.cn/read.php?tid=29551863&forder_by=postdatedesc&rand=656)，我前端这块比较菜，主要成果在评分系统的构建上，静态网页部分是在他的圣遗物强化助手网页的基础上加入了自己的评分系统。

## 评分公式

![](public/introduction.png)

整个圣遗物评分由两部分构成，主属性得分与有效词条数，主属性与副词条分别作为评价圣遗物的好坏的两个部分。后续或许会加入圣遗物套装参与评价，但是由于过于复杂并且大多数人不太会像我这样每套都刷一些，感觉需求不是特别大而且我也没想好，先挖个坑吧，大佬们有想法可以给我提建议。

### 主属性得分=主属性权重*属性使用率/属性出现概率。

主属性权重即为主属性的评分占整个评分的比例，是为了平衡主属性与副词条间的关系设置的。这个权重越大主属性比副词条越重要，有的人更重视主属性而有的人更重视副词条，可以根据个性化的需求进行设置。

属性使用率为使用该主属性圣遗物的角色占全角色的比例，反应的是某个主属性的圣遗物多少角色使用，使用这个主属性的角色越多说明该主属性的圣遗物需求量越大。最明显的例子是攻击沙，由于需要攻击沙的角色比需要防御生命沙的角色多很多，所以我会更倾向于保留更多的攻击沙，即使他们刷出来的难度是差不多的。因为属性使用率是截至2.4版本的统计结果，所以可能会有有一定的误差，统计模板来自[全角色圣遗物及武器搭配简述](https://ngabbs.com/read.php?tid=27859119)。但需要注意的是属性使用率的本质是用现有角色的需求状况预测以后出的角色总体需求状况，但事实上新出的角色更多的会区别于老角色的定位（像新出的申鹤需要攻击头而非暴击头将会拉高攻击头的整体使用率），所以这部分是整个模型中误差较大的部分，对未来可期的圣遗物评价有限。目前来说我没有想到一个更好的反应需求量的办法。

属性出现概率为主属性属性在该部位圣遗物的出现概率，反映的是该类型圣遗物的刷取难度。比如精通头虽然需要的角色很少，但是全游最低的掉率让很多人给万叶刷精通圣遗物的时候一头难求。这里的出现概率参考了[圣遗物词条分布和掉落分布的推测](https://bbs.nga.cn/read.php?tid=25954661)，是概率统计结果，可能会与官方概率有所偏差，但总体还是比较准确的。

下表为主属性权重为0.5时的主属性得分情况，这里的得分与词条数等价。如主属性权重为0.5时一个暴击头将相当于自带3.96个有效词条，一个防御沙需要比暴击头多3.76个有效副词条才能得到相同的评分。

| 部位   | 主属性        | 出现概率 | 使用概率 | 主属性得分 |
| ------ | ------------- | -------- | -------- | ---------- |
| 生之花 | 生命值        | 100.00%  | 100.00%  | 0.50       |
| 死之羽 | 攻击力        | 100.00%  | 100.00%  | 0.50       |
| 时之沙 | 攻击力        | 26.66%   | 72.92%   | 1.37       |
| 时之沙 | 生命值        | 26.66%   | 14.58%   | 0.27       |
| 时之沙 | 防御力        | 26.66%   | 10.42%   | 0.20       |
| 时之沙 | 元素充能      | 10.00%   | 58.33%   | 2.92       |
| 时之沙 | 元素精通      | 10.00%   | 22.92%   | 1.15       |
| 空之杯 | 攻击力        | 21.25%   | 29.17%   | 0.69       |
| 空之杯 | 生命值        | 21.25%   | 12.50%   | 0.29       |
| 空之杯 | 防御力        | 20.00%   | 8.33%    | 0.21       |
| 空之杯 | 物理/元素伤害 | 35.00%   | 79.17%   | 1.13       |
| 空之杯 | 元素精通      | 2.50%    | 14.58%   | 2.92       |
| 理之冠 | 攻击力        | 22.00%   | 16.66%   | 0.38       |
| 理之冠 | 生命值        | 22.00%   | 10.42%   | 0.24       |
| 理之冠 | 防御力        | 22.00%   | 8.33%    | 0.19       |
| 理之冠 | 暴击率        | 10.00%   | 79.17%   | 3.96       |
| 理之冠 | 暴击伤害      | 10.00%   | 77.08%   | 3.85       |
| 理之冠 | 治疗加成      | 10.00%   | 16.66%   | 0.83       |
| 理之冠 | 元素精通      | 4.00%    | 14.58%   | 1.82       |

### 有效词条数

这里介绍一下这个系统的前作，[单个圣遗物词条数计算器](https://bbs.nga.cn/read.php?tid=29672103)，因为要下载并且手动输入圣遗物副词条所以不太方便，不过如果需要看看刚强化出的单个圣遗物怎么样而不想扫描的话可以尝试一下。

这里沿用了之前依据主属性确定有效词条的计算公式，主属性被分为基础属性与通用属性，基础属性为攻击生命防御这三种属性，通用属性则是充能双爆等这种无论时攻击还是生命防御的角色都有可能需要的属性。

当主属性为基础属性时又分攻击与生命防御两种情况，主属性为攻击时生命防御视为无效词条不参与有效词条计算，为生命防御时攻击力词条额外乘攻击-生命（防御）转化率后参与词条计算。造成这种现象的原因是多数生命防御依赖型角色仍是将生命防御转化为攻击，只有少数（如阿贝多的E）技能是直接依赖于防御力。

主属性为通用属性时取副词条中最高的基础属性作为参考主属性，按照主属性为基础属性计算，真正实现时将分为两层计算，具体可至之前的帖子中查看。在无基础属性词条，即副词条为暴击爆伤充能精通时各词条按权重直接参与词条计算就可以了。

最后说下未满级圣遗物的期望计算，这里的计算方法使用了[圣遗物强化助手](https://github.com/ideless/artifact/tree/master/src/ys)中的计算方法，公式如下

特别的，由于三词条圣遗物词条数过少，在计算期望时将不再判断该词条是否有效。由此，在圣遗物等级较高时会有更好的效果，期望建议仅作为参考，较为不错的胚子可以强化到一定等级以后再做判断。

> In this section, only rarity 5 artifacts are considered.

Minor affixes are considered important to the evaluation of an artifact's
potential because main affixes are fixed. As minor affix increment takes
4 possible values, the affix number of a minor affix is defined to be the
ratio of its value divided by the maximum one-time increment of this
minor affix. The affix number of an artifact is defined to be an weighted
sum of each minor affix number, given the weight of each minor affix customed
by users. This is because certain minor affixes are considered useless while
others are usually more valuable. Weight of a minor affix must be between
0 and 1.

For an artifact, let $\alpha$ be the main affix, $a_{i}$ be a minor affix,
$A$ be the set of all minor affixes, $p( a_{i})$ be the pick weight,
$w( a_{i})$ be customized affix weight, $v^{*}( a_{i})$ be the maximum
one-time increment, and $v( a_{i})$ be the current affix value. Expected,
minimum and maximum affix numbers are refered to by
$\overline{S} ,S_{min} ,S_{max}$, respectively.

#### Artifacts with 3 minor affixes

Let $a_{1} ,a_{2} ,a_{3}$ be the 3 minor affixes. Affix enhancement times
$n=5$. Expected affix number is

$$
\begin{aligned}
\overline{S} = & \sum _{i=1,2,3} w( a_{i})\left(\frac{v( a_{i})}{v^{*}( a_{i})} +4\times \frac{1}{4} \times 0.85\right)\\
 & +\frac{\sum _{a\in A\backslash \{a_{1} ,a_{2} ,a_{3} ,\alpha \}} w( a) p( a)}{\sum _{a\in A\backslash \{a_{1} ,a_{2} ,a_{3} ,\alpha \}} p( a)} \times \left( 0.85+4\times \frac{1}{4} \times 0.85\right).
\end{aligned}
$$

#### Artifact with 4 minor affixes

Let $a_{1} ,a_{2} ,a_{3} ,a_{4}$ be the 4 minor affixes. Affix enhancement times is $n$.
Expected affix number is

$$
\overline{S} =\sum _{i=1,2,3,4} w( a_{i})\left(\frac{v( a_{i})}{v^{*}( a_{i})} +n\times \frac{1}{4} \times 0.85\right).
$$

## Project setup

In this section, please change to source branch.

```
npm install
```

### Compiles and hot-reloads for development

```
npm run serve
```

### Compiles and minifies for production

```
npm run build
```
