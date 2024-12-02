import {EventBus} from '@odoo/owl'
import {GAME_DATA} from './data'

export class Clicker {

    constructor(state) {
        this.state = state || {
            clicks: 0,
            xp: 0,
            level: 0,
            bots: {}
        }

        this.bus = new EventBus()
    }

    //==================================================================================================================

    get levelingStats() {
        const currentLevel = GAME_DATA.level(this.state.level)
        const nextLevel = GAME_DATA.level(this.state.level + 1)

        const levelGap = nextLevel.xp - currentLevel.xp
        const levelProgression = this.state.xp - currentLevel.xp

        return {
            levelGap: levelGap,
            levelProgression: levelProgression,
            levelPercentage: 100 * levelProgression / levelGap
        }
    }

    get bots() {
        const res = []
        for (const [bot_id, bot] of Object.entries(GAME_DATA.bots)) {
            res.push({
                id: bot_id,
                spec: bot,
                price: GAME_DATA.bots[bot_id].price(this.state.bots[bot_id] || 0),
                number: this.state.bots[bot_id] || 0,
                unlocked: bot.unlocked(this.state.level, this.state.bots),
                producing: GAME_DATA.bots[bot_id].produces * (this.state.bots[bot_id] || 0)
            })
        }
        return res
    }

    _runBots() {
        let clicks = 0
        for (const bot of this.bots) {
            clicks += bot.spec.produces * bot.number
        }
        if (clicks > 0)
            this.increment(clicks)
    }

    //==================================================================================================================

    _progress() {
        const nextLevel = GAME_DATA.level(this.state.level + 1)
        if (this.state.xp >= nextLevel.xp) {
            this.state.level += 1
            this.bus.trigger("LEVEL", {level: this.state.level, ...GAME_DATA.level(this.state.level)})
        }
    }

    tick() {
        this._runBots()
        this._progress()
    }

    //==================================================================================================================

    increment(inc = 1) {
        this.state.clicks += inc
        this.state.xp += inc
    }

    buyBot(bot_id) {
        if (GAME_DATA.bots.hasOwnProperty(bot_id) &&
            GAME_DATA.bots[bot_id].unlocked(this.state.level, this.state.bots) &&
            this.state.clicks >= GAME_DATA.bots[bot_id].price(this.state.bots[bot_id] || 0)) {

            this.state.clicks -= GAME_DATA.bots[bot_id].price(this.state.bots[bot_id] || 0)
            this.state.bots[bot_id] = (this.state.bots[bot_id] || 0) + 1

        }
    }
}