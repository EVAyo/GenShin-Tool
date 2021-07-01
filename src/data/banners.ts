interface Banner {
  name: string;
  shortName: string;
  image: number;
  start: string;
  end: string;
  color: string;
  featured?: string[];
  featuredRare?: string[];
  timezoneDependent?: boolean;
}

export const banners: {[key: number]: Banner} = {
  100001: {
    name: "Beginners' Wish",
    shortName: "Beginners' Wish",
    image: 1,
    start: '2000-01-01 00:00:00',
    end: '2200-01-01 00:00:00',
    color: '#FFFFFF',
  },

  200001: {
    name: 'Wanderlust Invocation',
    shortName: 'Wanderlust Invocation',
    image: 1,
    start: '2000-01-01 00:00:00',
    end: '2200-01-01 00:00:00',
    color: '#FFFFFF',
  },

  300001: {
    name: 'Ballad in Goblets',
    image: 1,
    shortName: 'Venti',
    start: '2020-09-28 00:00:00',
    end: '2020-10-18 18:00:00',
    color: '#55E4B0',
    timezoneDependent: true,
    featured: ['venti'],
  },
  300002: {
    name: 'Sparkling Steps',
    image: 1,
    shortName: 'Klee',
    start: '2020-10-20 18:00:00',
    end: '2020-11-10 16:00:00',
    color: '#CA360E',
    featured: ['klee'],
  },
  300003: {
    name: 'Farewell of Snezhnaya',
    image: 1,
    shortName: 'Tartaglia',
    start: '2020-11-11 06:00:00',
    end: '2020-12-01 16:00:00',
    color: '#50A3C0',
    timezoneDependent: true,
    featured: ['tartaglia'],
  },
  300004: {
    name: 'Gentry of Hermitage',
    image: 1,
    shortName: 'Zhongli',
    start: '2020-12-01 18:00:00',
    end: '2020-12-22 15:00:00',
    color: '#D1A55C',
    featured: ['zhongli'],
  },
  300005: {
    name: 'Secretum Secretorum',
    image: 1,
    shortName: 'Albedo',
    start: '2020-12-23 06:00:00',
    end: '2021-01-12 16:00:00',
    color: '#FCFE83',
    timezoneDependent: true,
    featured: ['albedo'],
  },
  300006: {
    name: 'Adrift in the Harbor',
    image: 1,
    shortName: 'Ganyu',
    start: '2021-01-12 18:00:00',
    end: '2021-02-02 15:00:00',
    color: '#6994DF',
    featured: ['ganyu'],
  },
  300007: {
    name: 'Invitation to Mundane Life',
    image: 1,
    shortName: 'Xiao',
    start: '2021-02-03 06:00:00',
    end: '2021-02-17 16:00:00',
    color: '#2BE3F8',
    timezoneDependent: true,
    featured: ['xiao'],
  },
  300008: {
    name: 'Dance of Lanterns',
    image: 1,
    shortName: 'Keqing',
    start: '2021-02-17 18:00:00',
    end: '2021-03-02 16:00:00',
    color: '#AB6CD7',
    featured: ['keqing'],
  },
  300009: {
    name: 'Moment of Bloom',
    image: 1,
    shortName: 'Hu Tao',
    start: '2021-03-02 18:00:00',
    end: '2021-03-16 15:00:00',
    color: '#BF5042',
    featured: ['hu_tao'],
  },
  300010: {
    name: 'Ballad in Goblets',
    image: 2,
    shortName: 'Venti',
    start: '2021-03-17 06:00:00',
    end: '2021-04-06 16:00:00',
    color: '#35C297',
    featured: ['venti'],
    featuredRare: ['sucrose', 'razor', 'noelle'],
    timezoneDependent: true,
  },
  300011: {
    name: 'Farewell of Snezhnaya',
    image: 2,
    shortName: 'Tartaglia',
    start: '2021-04-06 18:00:00',
    end: '2021-04-27 15:00:00',
    color: '#50A3C0',
    featured: ['tartaglia'],
    featuredRare: ['rosaria', 'fischl', 'barbara'],
  },
  300012: {
    name: 'Gentry of Hermitage',
    image: 2,
    shortName: 'Zhongli',
    start: '2021-04-28 06:00:00',
    end: '2021-05-18 17:59:59',
    color: '#D1A55C',
    featured: ['zhongli'],
    featuredRare: ['yanfei', 'noelle', 'diona'],
    timezoneDependent: true,
  },
  300013: {
    name: 'Born of Ocean Swell',
    image: 1,
    shortName: 'Eula',
    start: '2021-05-18 18:00:00',
    end: '2021-06-08 15:00:00',
    color: '#A6D6E0',
    featured: ['eula'],
    featuredRare: ['xingqiu', 'beidou', 'xinyan'],
  },
  300014: {
    name: 'Sparkling Steps',
    image: 2,
    shortName: 'Klee',
    start: '2021-06-09 06:00:00',
    end: '2021-06-29 17:59:59',
    color: '#CA360E',
    featured: ['klee'],
    featuredRare: ['fischl', 'sucrose', 'barbara'],
    timezoneDependent: true,
  },
  300015: {
    name: 'Leaves in the Wind',
    image: 1,
    shortName: 'Kazuha',
    start: '2021-06-29 18:00:00',
    end: '2021-07-20 14:59:59',
    color: '#8FFFDE',
    featured: ['kaedehara_kazuha'],
    featuredRare: ['bennett', 'razor', 'rosaria'],
  },

  400001: {
    name: 'Epitome Invocation',
    image: 1,
    start: '2020-09-28 00:00:00',
    end: '2020-10-18 18:00:00',
    shortName: 'Amos',
    color: '#f54e42',
    timezoneDependent: true,
    featured: ['aquila_favonia', 'amos_bow'],
  },
  400002: {
    name: 'Epitome Invocation',
    image: 2,
    start: '2020-10-20 18:00:00',
    end: '2020-11-10 16:00:00',
    shortName: 'Lost Prayer',
    color: '#f5c242',
    featured: ['lost_prayer_to_the_sacred_winds', 'wolfs_gravestone'],
  },
  400003: {
    name: 'Epitome Invocation',
    image: 3,
    start: '2020-11-11 06:00:00',
    end: '2020-12-01 16:00:00',
    shortName: 'Skyward',
    color: '#f5ef42',
    timezoneDependent: true,
    featured: ['skyward_harp', 'memory_of_dust'],
  },
  400004: {
    name: 'Epitome Invocation',
    image: 4,
    start: '2020-12-01 18:00:00',
    end: '2020-12-22 15:00:00',
    shortName: 'Vortex',
    color: '#7ef542',
    featured: ['vortex_vanquisher', 'the_unforged'],
  },
  400005: {
    name: 'Epitome Invocation',
    image: 5,
    start: '2020-12-23 06:00:00',
    end: '2021-01-12 16:00:00',
    shortName: 'Summit',
    color: '#42ecf5',
    timezoneDependent: true,
    featured: ['summit_shaper', 'skyward_atlas'],
  },
  400006: {
    name: 'Epitome Invocation',
    image: 6,
    start: '2021-01-12 18:00:00',
    end: '2021-02-02 15:00:00',
    shortName: 'Amos',
    color: '#424ef5',
    featured: ['amos_bow', 'skyward_pride'],
  },
  400007: {
    name: 'Epitome Invocation',
    image: 7,
    start: '2021-02-03 06:00:00',
    end: '2021-02-23 16:00:00',
    shortName: 'Primordial',
    color: '#b042f5',
    timezoneDependent: true,
    featured: ['primordial_jade_winged-spear', 'primordial_jade_cutter'],
  },
  400008: {
    name: 'Epitome Invocation',
    image: 8,
    start: '2021-02-23 18:00:00',
    end: '2021-03-16 15:00:00',
    shortName: 'Homa',
    color: '#f542c8',
    featured: ['wolfs_gravestone', 'staff_of_homa'],
  },
  400009: {
    name: 'Epitome Invocation',
    image: 9,
    start: '2021-03-17 06:00:00',
    end: '2021-04-06 16:00:00',
    shortName: 'Elegy',
    color: '#f54e42',
    timezoneDependent: true,
    featured: ['elegy_for_the_end', 'skyward_blade'],
    featuredRare: [
      'the_alley_flash',
      'wine_and_song',
      'favonius_greatsword',
      'favonius_warbow',
      'dragons_bane',
    ],
  },
  400010: {
    name: 'Epitome Invocation',
    image: 10,
    start: '2021-04-06 18:00:00',
    end: '2021-04-27 15:00:00',
    shortName: 'Skyward',
    color: '#f5c242',
    featured: ['skyward_harp', 'lost_prayer_to_the_sacred_winds'],
    featuredRare: [
      'alley_hunter',
      'favonius_codex',
      'favonius_lance',
      'sacrificial_greatsword',
      'favonius_sword',
    ],
  },
  400011: {
    name: 'Epitome Invocation',
    image: 11,
    start: '2021-04-28 06:00:00',
    end: '2021-05-18 17:59:59',
    shortName: 'Summit',
    color: '#f5ef42',
    timezoneDependent: true,
    featured: ['summit_shaper', 'memory_of_dust'],
    featuredRare: [
      'lithic_blade',
      'lithic_spear',
      'sacrificial_bow',
      'eye_of_perception',
      'the_flute',
    ],
  },
  400012: {
    name: 'Epitome Invocation',
    image: 12,
    start: '2021-05-18 18:00:00',
    end: '2021-06-08 15:00:00',
    shortName: 'Pines',
    color: '#7ef542',
    featured: ['song_of_broken_pines', 'aquila_favonia'],
    featuredRare: [
      'rust',
      'sacrificial_fragments',
      'dragons_bane',
      'rainslasher',
      'sacrificial_sword',
    ],
  },
  400013: {
    name: 'Epitome Invocation',
    image: 13,
    start: '2021-06-09 06:00:00',
    end: '2021-06-29 17:59:59',
    shortName: 'Lost Prayer',
    color: '#42ecf5',
    featured: ['lost_prayer_to_the_sacred_winds', 'skyward_pride'],
    featuredRare: [
      'mitternachts_waltz',
      'lions_roar',
      'the_bell',
      'favonius_lance',
      'the_widsith',
    ],
    timezoneDependent: true,
  },
  400014: {
    name: 'Epitome Invocation',
    image: 14,
    start: '2021-06-29 18:00:00',
    end: '2021-07-20 14:59:59',
    shortName: 'Freedom-Sworn',
    color: '#42ecf5',
    featured: ['freedom-sworn', 'skyward_atlas'],
    featuredRare: ['the_alley_flash', 'wine_and_song', 'alley_hunter', 'favonius_greatsword', 'dragons_bane'],
  },
};
