var app1 = new Vue({
	el: '#app1',
	data: {
		gongjili: 2173, //攻击力
		baojilv: 89.6, //暴击率%
		baojishanghai: 157.1, //暴击伤害%
		jinengbeilv: 656, //技能倍率%
		juesedengji: 90, //角色等级
		guaiwudengji: 86, //怪物等级
		yuansuzengshang: 46.4, //元素增伤%
		wuqizegnshang: 20, //武器增伤%
		shengyiwu: 35, //圣遗物增伤%
		jiankang: 20, //减抗%
		guaiwukangxing: 10, //怪物默认抗性%
		jianfang: 0, //减防%
		fanying: 1, //元素反应
		fanyingjiacheng: 32 //反应倍率加成%
	},
	computed: {
		//防御系数
		fangyuxishu: function() {
			return (parseInt(this.juesedengji) + 100) / ((this.juesedengji + 100) + (this.guaiwudengji + 100) * (1 -
				this.jianfang / 100));
		},
		shanghai1: function() {
			var kangxing2 = 0; //等下要用到的抗性增伤系数
			var fanyingjiacheng2 = 0; //如果不参与元素反应，则0加成

			if (this.jiankang > 0) {
				//如果减抗后，为负数
				if (this.jiankang - this.guaiwukangxing > 0) {
					kangxing2 = -(this.jiankang - this.guaiwukangxing) / 2;
				} else {
					kangxing2 = this.jiankang - this.guaiwukangxing;
				}
			} else {
				kangxing2 = this.guaiwukangxing; //怪物默认抗性
			}

			if (this.fanying == 1) {
				fanyingjiacheng2 = 0;
			} else {
				fanyingjiacheng2 = this.fanyingjiacheng;
			}

			return this.gongjili * //攻击力
				(this.jinengbeilv / 100) * //技能倍率
				(1 + this.yuansuzengshang / 100 + this.wuqizegnshang / 100 + this.shengyiwu / 100) * //增伤
				(1 - kangxing2 / 100) * //抗性
				((this.juesedengji + 100) / ((this.juesedengji + 100) + (this
					.guaiwudengji + 100) * (1 - this.jianfang / 100))) * //等级防御力
				(this.fanying) * (1 + fanyingjiacheng2 / 100) //元素反应倍率
		},
		shanghai2: function() {
			var kangxing2 = 0; //等下要用到的抗性增伤系数
			var fanyingjiacheng2 = 0; //如果不参与元素反应，则0加成
		
			if (this.jiankang > 0) {
				//如果减抗后，为负数
				if (this.jiankang - this.guaiwukangxing > 0) {
					kangxing2 = -(this.jiankang - this.guaiwukangxing) / 2;
				} else {
					kangxing2 = this.jiankang - this.guaiwukangxing;
				}
			} else {
				kangxing2 = this.guaiwukangxing; //怪物默认抗性
			}
		
			if (this.fanying == 1) {
				fanyingjiacheng2 = 0;
			} else {
				fanyingjiacheng2 = this.fanyingjiacheng;
			}
		
			return this.gongjili * //攻击力
				(this.jinengbeilv / 100) * //技能倍率
				(1 + (this.baojishanghai / 100)) * //暴击暴伤
				(1 + this.yuansuzengshang / 100 + this.wuqizegnshang / 100 + this.shengyiwu / 100) * //增伤
				(1 - kangxing2 / 100) * //抗性
				((this.juesedengji + 100) / ((this.juesedengji + 100) + (this
					.guaiwudengji + 100) * (1 - this.jianfang / 100))) * //等级防御力
				(this.fanying) * (1 + fanyingjiacheng2 / 100) //元素反应倍率
		},
		shanghai3: function() {
			var kangxing2 = 0; //等下要用到的抗性增伤系数
			var fanyingjiacheng2 = 0; //如果不参与元素反应，则0加成
		
			if (this.jiankang > 0) {
				//如果减抗后，为负数
				if (this.jiankang - this.guaiwukangxing > 0) {
					kangxing2 = -(this.jiankang - this.guaiwukangxing) / 2;
				} else {
					kangxing2 = this.jiankang - this.guaiwukangxing;
				}
			} else {
				kangxing2 = this.guaiwukangxing; //怪物默认抗性
			}
		
			if (this.fanying == 1) {
				fanyingjiacheng2 = 0;
			} else {
				fanyingjiacheng2 = this.fanyingjiacheng;
			}
		
			return this.gongjili * //攻击力
				(this.jinengbeilv / 100) * //技能倍率
				(1 + (this.baojilv / 100) * (this.baojishanghai / 100)) * //暴击暴伤
				(1 + this.yuansuzengshang / 100 + this.wuqizegnshang / 100 + this.shengyiwu / 100) * //增伤
				(1 - kangxing2 / 100) * //抗性
				((this.juesedengji + 100) / ((this.juesedengji + 100) + (this
					.guaiwudengji + 100) * (1 - this.jianfang / 100))) * //等级防御力
				(this.fanying) * (1 + fanyingjiacheng2 / 100) //元素反应倍率
		}
	}
});