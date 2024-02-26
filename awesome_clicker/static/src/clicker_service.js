/** @odoo-module **/

import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

const clickerService = {
  dependencies: [],
  start() {
    const state = reactive({ count: 1000, level: 1, bots: 0 });

    document.addEventListener("click", () => state.count++, true);

    setInterval(() => (state.count += 10 * state.bots), 10 * 1000);

    return {
      state,
      increment(inc) {
        state.count += inc;
      },
      buyBot() {
        if (state.count < 1000) return;
        state.bots++;
        state.count -= 1000;
      },
    };
  },
};

registry
  .category("services")
  .add("awesome_clicker.clickerService", clickerService);
