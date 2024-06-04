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
        this.totalCps = 0;
        this._updateTimeout = undefined;
        this._lastUpdateTimestamp = Date.now();
        this._eventBus = new EventBus();

        this.setupData(...arguments);
        this.setupEffects(...arguments);
    }

    setupData() {
        this.autoclickers = { ...autoclickers };
        this.achievements = [...achievements];
        this.upgrades = [...upgrades];
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
        const price = autoclicker.getPriceForNextAmount(amount);
        if (this.clickBalance >= price) {
            this.clickBalance -= price;
            autoclicker.amountPurchased += amount;
            this._update();
        }
    }

    purchaseUpgrade(upgradeName) {
        const upgrade = this.upgrades.find(upgrade => upgrade.name === upgradeName);
        if (!upgrade) {
            throw new Error(`No such upgrade: ${upgradeName}`);
        }
        const price = upgrade.price;
        if (this.clickBalance >= price) {
            this.clickBalance -= price;
            upgrade.buy(this);
            this._update();
        }
    }

    canAfford(autoclickerName, amount) {
        const autoclicker = this.autoclickers[autoclickerName];
        const price = autoclicker.getPriceForNextAmount(amount);
        return this.clickBalance >= price;
    }

    canAffordUpgrade(upgradeName) {
        const upgrade = this.upgrades.find(upgrade => upgrade.name === upgradeName);
        if (!upgrade) {
            throw new Error(`No such upgrade: ${upgradeName}`);
        }
        return this.clickBalance >= upgrade.price;
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
        this._unlockUpgrades();
        this._unlockAchievements();

        this.totalCps = this._getTotalCpms() * 1000;

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

    _unlockUpgrades() {
        for (const upgrade of this.upgrades) {
            if (upgrade.shouldUnlock(this)) {
                upgrade.unlock();
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
        this.cpsMultiplier = 1;
    }

    get baseCpms() {
        return this.baseIncomePerAutoClick / this.autoClickInterval;
    }

    get cpms() {
        return this.baseCpms * this.cpsMultiplier;
    }

    get totalCpms() {
        return this.cpms * this.amountPurchased;
    }

    get baseCps() {
        return this.baseCpms * 1000;
    }

    get cps() {
        return this.cpms * 1000;
    }

    get totalCps() {
        return this.totalCpms * 1000;
    }

    get nextPrice() {
        return this.getPriceForNextAmount(1);
    }

    getPriceForNextAmount(amount) {
        const targetLevel = this.amountPurchased + amount;
        let price = 0;
        for (let level = this.amountPurchased + 1; level <= targetLevel; level++) {
            price += this.getPriceForLevel(level);
        }
        return price;
    }

    getPriceForLevel(level) {
        if (level <= 0) return 0;
        return Math.floor(Math.pow(this.basePrice, (1 + 0.1 * (level - 1))));
    }

    /**
     * @param type {'cps_multiplier'}
     * @param modifier {Function}
     */
    addModifier(type, modifier) {
        switch (type) {
            case "cps_multiplier":
                this.cpsMultiplier = modifier(this.cpsMultiplier);
                break;
            default:
                throw new Error(`No such modifier type: ${type}`);
        }
    }
}

class ClickerUpgrade {
    constructor(name, string, description, price, shouldUnlock, applyModifiers) {
        this.name = name;
        this.string = _lt(string);
        this.description = _lt(description);
        this.price = price;
        this.unlocked = false;
        this.isPurchased = false;
        this._shouldUnlock = shouldUnlock;
        this._applyModifiers = applyModifiers;
    }

    shouldUnlock(clickerStore) {
        return this._shouldUnlock(clickerStore);
    }

    unlock() {
        this.unlocked = true;
    }

    buy(clickerStore) {
        if (this.unlocked && !this.isPurchased) {
            this._applyModifiers(clickerStore);
            this.isPurchased = true;
        }
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
        10,
        10 * 1000,
        1,
    ),
    clickBotMax: new ClickerAutoClicker(
        "Click Bot Max:tm:",
        100,
        30 * 1000,
        10,
    ),
};

const upgrades = [
    new ClickerUpgrade(
        "click_bot_1",
        "Improved Click Bots",
        "Click Bots are twice as efficient",
        500,
        clickerStore => {
            return clickerStore.clickBalance >= 200;
        },
        clickerStore => {
            clickerStore.autoclickers.clickBot.addModifier("cps_multiplier", (value) => value * 2);
        },
    ),
];

const achievements = [
    new ClickerAchievement(
        "click_bot_1",
        "Handcrafted",
        "Unlock click bots",
        (clickerStore) => !!clickerStore.autoclickers.clickBot.unlocked,
    ),
    new ClickerAchievement(
        "click_bot_max_1",
        "Handcrafted",
        "Unlock the Click Bot Max:tm:",
        (clickerStore) => !!clickerStore.autoclickers.clickBot.unlocked,
    ),
];

const effectTypes = {
    showRainbowperson: (effectService, achievement, payload) => {
        effectService.add({
            type: "rainbow_man",
            message: payload,
        });
    },
};

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
