export class UnlockCondition {
    valid(level, bots) {
        return true
    }
}

export class AndUnlock extends UnlockCondition {
    constructor(...conditions) {
        super();
        this.conditions = conditions;
    }

    valid(level, bots) {
        return this.conditions.every((c) => c.valid(level, bots))
    }
}

export class OrUnlock extends UnlockCondition {
    constructor(...conditions) {
        super();
        this.conditions = conditions;
    }

    valid(level, bots) {
        return this.conditions.some((c) => c.valid(level, bots))
    }
}

export class LevelUnlock extends UnlockCondition {
    constructor(level) {
        super();
        this.level = level;
    }

    valid(level, bots) {
        return level >= this.level
    }
}

export class BotUnlock extends UnlockCondition {
    constructor(bot_id, number) {
        super();
        this.bot_id = bot_id;
        this.number = number;
    }

    valid(level, bots) {
        return (bots[this.bot_id] || 0) >= this.number
    }
}

class Bot {
    constructor(name, produces, unlock, base_price, icon) {
        this.name = name
        this.produces = produces
        this.unlock = unlock
        this.base_price = base_price
        this.icon = icon
    }

    unlocked(level, bots) {
        return this.unlock.valid(level, bots)
    }

    price(numberBought) {
        return Math.round(this.base_price * Math.pow(1.15, numberBought))
    }
}

export const GAME_DATA = {
    bots: {
        bot_0: new Bot(
            'Cursor',
            0.1,
            new LevelUnlock(1),
            15,
            'fa-hand-pointer-o'
        ),
        bot_1: new Bot(
            'Bot',
            1,
            new LevelUnlock(2),
            100,
            'fa-android'
        ),
        bot_2: new Bot(
            'House',
            8,
            new LevelUnlock(3),
            1_100,
            'fa-home'
        ),
        bot_3: new Bot(
            'Mansion',
            47,
            new LevelUnlock(4),
            12_000,
            'fa-fort-awesome'
        ),
        bot_4: new Bot(
            'Factory',
            260,
            new LevelUnlock(5),
            130_000,
            'fa-industry'
        ),
        bot_5: new Bot(
            'Temple',
            1_400,
            new LevelUnlock(6),
            1_400_000,
            'fa-institution'
        ),
        bot_6: new Bot(
            'City',
            7_800,
            new LevelUnlock(7),
            20_000_000,
            'fa-building'
        ),
        bot_7: new Bot(
            'Rocket',
            44_000,
            new LevelUnlock(8),
            330_000_000,
            'fa-rocket'
        ),
        bot_8: new Bot(
            'Planet',
            260_000,
            new LevelUnlock(9),
            5_100_000_000,
            'fa-globe'
        ),
        bot_9: new Bot(
            'Star',
            1_600_000,
            new LevelUnlock(10),
            75_000_000_000,
            'fa-star'
        ),
        bot_10: new Bot(
            'Galaxy',
            10_000_000,
            new LevelUnlock(11),
            1_000_000_000_000,
            'fa-superpowers'
        ),
        bot_11: new Bot(
            'Universe',
            65_000_000,
            new LevelUnlock(12),
            14_000_000_000_000,
            'fa-jsfiddle'
        ),

    },

    levelScale: [
        {xp: 0},
        {xp: 15, message: 'You can now buy Cursors !'},
        {xp: 320, message: 'You can now buy Bots !'},
        {xp: 2_350, message: 'You can now buy Houses !'},
        {xp: 24_500, message: 'You can now buy Mansions !'},
        {xp: 268_000, message: 'You can now buy Factories !'},
        {xp: 2_900_000, message: 'You can now buy Temples !'},
        {xp: 31_300_000, message: 'You can now buy Cities !'},
        {xp: 437_000_000, message: 'You can now buy Rockets !'},
        {xp: 7_130_000_000, message: 'You can now buy Planets !'},
        {xp: 110_000_000_000, message: 'You can now buy Stars !'},
        {xp: 1_630_000_000_000, message: 'You can now buy Galaxies !'},
        {xp: 21_900_000_000_000, message: 'You can now buy Universes !'},
    ],

    tick: 1000,

    level(num) {
        return this.levelScale[num] || {xp: Infinity}
    }
}