/** @odoo-module **/

import { EventBus } from "@odoo/owl";
import { _lt } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { Reactive } from "@web/core/utils/reactive";


const EVENT_ACHIEVEMENT_UNLOCKED = "achievement.unlocked";

class ClickerStore extends Reactive {
    static serviceDependencies = ['effect'];

    constructor() {
        super();
        this.setup(...arguments);
    }

    setup() {
        this.clickBalance = 0;
        this._updateTimeout = undefined;
        this._lastUpdateTimestamp = Date.now();
        this._eventBus = new EventBus();

        this.setupData(...arguments);
        this.setupEffects(...arguments);
    }

    setupData() {
        this.autoclickers = { ...autoclickers };
        this.achievements = [...achievements];
    }

    setupEffects(env, { effect: effectService }) {
        for (const effect of effects) {
            this._eventBus.addEventListener(effect.event, event => {
                if (effect.matches(event.detail)) {
                    effect.type(effectService, event.achievement, effect.payload);
                }
            });
        }
    }

    increment(amount = 1) {
        this.clickBalance += amount;
        this._update();
    }

    purchaseAutoclicker(autoclickerName, amount = 1) {
        const autoclicker = this.autoclickers[autoclickerName];
        const price = autoclicker.price * amount;
        if (this.clickBalance >= price) {
            this.clickBalance -= price;
            autoclicker.amountPurchased += amount;
            this._update();
        }
    }

    canAfford(autoclickerName, amount) {
        const autoclicker = this.autoclickers[autoclickerName];
        const price = autoclicker.price * amount;
        return this.clickBalance >= price;
    }

    _getTotalCpms() {
        return Object.values(this.autoclickers).map(autoclicker => autoclicker.totalCpms)
            .reduce((v1, v2) => v1 + v2);
    }

    _scheduleNextUpdate() {
        if (this._updateTimeout) {
            clearTimeout(this._updateTimeout);
        }

        const totalCpms = this._getTotalCpms();
        const maximumUpdateInterval = totalCpms === 0 ? 60 * 1000 : Math.max(50, 1 / totalCpms);
        const nextUpdateTimeout = maximumUpdateInterval - (Date.now() - this._lastUpdateTimestamp);

        this._updateTimeout = setTimeout(() => this._update(), nextUpdateTimeout);
    }

    _update() {
        const delta = Date.now() - this._lastUpdateTimestamp;

        const clickDelta = this._getTotalCpms() * delta;
        this.clickBalance += clickDelta;

        this._unlockAutoclickers();
        this._unlockAchievements();

        this._lastUpdateTimestamp = Date.now();
        this._scheduleNextUpdate();
    }

    _unlockAutoclickers() {
        for (const autoclickerName in this.autoclickers) {
            const autoclicker = this.autoclickers[autoclickerName];
            if (this.clickBalance >= autoclicker.basePrice) {
                autoclicker.unlocked = true;
            }
        }
    }

    _unlockAchievements() {
        for (const achievement of this.achievements) {
            if (achievement.shouldUnlock(this)) {
                achievement.unlock();
                this._eventBus.trigger(EVENT_ACHIEVEMENT_UNLOCKED, {
                    achievement: achievement,
                });
            }
        }
    }
}

class ClickerAutoClicker extends Reactive {
    constructor(string, basePrice, autoClickInterval, baseIncomePerAutoClick) {
        super();
        this.string = _lt(string);
        this.basePrice = basePrice;
        this.autoClickInterval = autoClickInterval;
        this.baseIncomePerAutoClick = baseIncomePerAutoClick;
        this.unlocked = false;
        this.amountPurchased = 0;
    }

    get cps() {
        return this.baseIncomePerAutoClick / this.autoClickInterval * 1000;
    }

    get cpms() {
        return this.baseIncomePerAutoClick / this.autoClickInterval;
    }

    get totalCps() {
        return this.cps * this.amountPurchased;
    }

    get totalCpms() {
        return this.cpms * this.amountPurchased;
    }

    get price() {
        return this.basePrice;
    }
}

class ClickerAchievement {
    constructor(name, string, description, shouldTrigger) {
        this.name = name;
        this.string = _lt(string);
        this.description = _lt(description);
        this._shouldTrigger = shouldTrigger;

        this.unlocked = false;
    }

    shouldUnlock(clickerStore) {
        return !this.unlocked && this._shouldTrigger(clickerStore);
    }

    unlock() {
        this.unlocked = true;
    }
}

const autoclickers = {
    clickBot: new ClickerAutoClicker(
        "Click Bot",
        100,
        10 * 1000,
        1,
    ),
};

const effectTypes = {
    showRainbowperson: (effectService, achievement, payload) => {
        effectService.add({
            type: "rainbow_man",
            message: payload,
        });
    },
};

const achievements = [
    new ClickerAchievement(
        "click_bot_1",
        "Handcrafted",
        "Unlock click bots",
        (clickerStore) => !!clickerStore.autoclickers.clickBot.unlocked,
    ),
];

const effects = [
    {
        type: effectTypes.showRainbowperson,
        event: EVENT_ACHIEVEMENT_UNLOCKED,
        matches: (event) => event.achievement.name === 'click_bot_1',
        payload: _lt(`Congrats on reaching ${autoclickers.clickBot.basePrice} clicks! You can now purchase click bots.`),
    }
];

const clickerService = {
    dependencies: ClickerStore.serviceDependencies,
    start(env, dependencies) {
        return new ClickerStore(env, dependencies);
    }
};

registry.category("services").add("awesome_clicker.clicker_service", clickerService);
