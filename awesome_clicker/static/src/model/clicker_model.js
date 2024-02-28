/* @odoo-module */

import { Reactive } from "@web/core/utils/reactive";
import { EventBus } from "@odoo/owl";
import { rewards } from "../clicker_rewards";
import { choose } from "../utils";

const MILESTONES = [
  { countRequired: 1000, unlock: "clickBot" },
  { countRequired: 5000, unlock: "bigBot" },
  { countRequired: 100000, unlock: "power multiplier" },
  { countRequired: 1000000, unlock: "pear tree & cherry tree" },
];

export class Clicker extends Reactive {
  constructor() {
    super();
    this.setup();
  }

  setup() {
    this.count = 1000000000;
    this.level = 1;
    this.power = 1;
    this.bots = {
      clickbot: {
        price: 1000,
        levelRequirment: 1,
        amountIncrease: 10,
        have: 0,
      },
      bigbot: {
        price: 5000,
        levelRequirment: 2,
        amountIncrease: 100,
        have: 0,
      },
    };
    this.trees = {
      pearTree: {
        price: 1000000,
        level: 4,
        produce: "pear",
        purchased: 0,
      },
      cherryTree: {
        price: 1000000,
        level: 4,
        produce: "cherry",
        purchased: 0,
      },
    };
    this.fruits = {
      pear: 0,
      cherry: 0,
    };
    this.eventBus = new EventBus();

    document.addEventListener("click", () => this.increment(1), true);
    setInterval(
      () =>
        Object.values(this.bots).forEach(
          (bot) => (this.count += bot.amountIncrease * bot.have * this.power)
        ),
      10 * 1000
    );
    setInterval(() => {
      Object.keys(this.trees).forEach(
        (tree) =>
          (this.fruits[this.trees[tree].produce] += this.trees[tree].purchased)
      );
    }, 30 * 1000);
  }

  increment(inc) {
    this.count += inc;
    if (
      MILESTONES[this.level] &&
      this.count >= MILESTONES[this.level].countRequired
    ) {
      this.eventBus.trigger("MILESTONE", MILESTONES[this.level]);
      this.level += 1;
    }
    if (this.count >= 1000 && this.level === 0) {
      this.eventBus.trigger("MILESTONE_1k");
      this.level++;
    }
  }

  addBot(type, amount) {
    if (!Object.keys(this.bots).includes(type)) {
      throw new Error(`Invalid bot name: ${type}`);
    }

    this.bots[type].have += amount;
  }

  buyBot(type) {
    if (!Object.keys(this.bots).includes(type)) {
      throw new Error(`Invalid bot name: ${type}`);
    }
    if (this.count < this.bots[type].price) return;

    this.count -= this.bots[type].price;
    this.bots[type].have += 1;
  }

  buyTree(name) {
    if (!Object.keys(this.trees).includes(name)) {
      throw new Error(`Invalid tree name ${name}`);
    }
    if (this.count < this.trees[name].price) {
      return false;
    }
    this.count -= this.trees[name].price;
    this.trees[name].purchased += 1;
  }

  buyMultiplier() {
    if (this.clicks < 50000) return;

    this.clicks -= 50000;
    this.power++;
  }

  giveReward() {
    const availableRewards = rewards.filter(
      (reward) =>
        (reward.minLevel <= this.level || !reward.minLevel) &&
        (reward.maxLevel >= this.level || !reward.maxLevel)
    );
    const reward = choose(availableRewards);
    this.eventBus.trigger("REWARD", reward);

    return reward;
  }
}
