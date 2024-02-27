/* @odoo-module */

import { Reactive } from "@web/core/utils/reactive";
import { EventBus } from "@odoo/owl";

const MILESTONES = [
  { countRequired: 1000, unlock: "clickBot" },
  { countRequired: 5000, unlock: "bigBot" },
  { clicks: 100000, unlock: "power multiplier" },
];

export class Clicker extends Reactive {
  constructor() {
    super();
    this.setup();
  }

  setup() {
    this.count = 0;
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
    this.eventBus = new EventBus();

    document.addEventListener("click", () => this.increment(1), true);
    setInterval(
      () =>
        Object.values(this.bots).forEach(
          (bot) => (this.count += bot.amountIncrease * bot.have * this.power)
        ),
      10 * 1000
    );
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

  buyBot(type) {
    if (!Object.keys(this.bots).includes(type)) {
      throw new Error(`Invalid bot name: ${type}`);
    }
    if (this.count < this.bots[type].price) return;

    this.count -= this.bots[type].price;
    this.bots[type].have += 1;
  }

  buyMultiplier() {
    if (this.clicks < 50000) return;

    this.clicks -= 50000;
    this.power++;
  }
}
