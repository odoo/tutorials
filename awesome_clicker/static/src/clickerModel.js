import { Reactive } from "@web/core/utils/reactive";

export class ClickerModel extends Reactive {
  constructor(initial = {}) {
    super();  
    this.clicks = initial.clicks || 0;
    this.level  = initial.level  || 0;
    this.clickBots = initial.clickBots || 0;
  }

  increment(amount) {
    this.clicks += amount;
  }

  computeAutoClicks() {
    if (this.clickBots > 0) {
      this.clicks += this.clickBots * 10;
    }
  }

  buyClickBot() {
    if (this.canBuyBot) {
      this.clickBots += 1;
      this.clicks -= 1000;
    }
    else {
        throw new Error("Not enough clicks to buy a Click Bot");
    }
  }

  get canBuyBot() {
    return this.clicks >= 1000;
  }
  get clickBotsVisible() {
    return this.level >= 1;
  }
}
