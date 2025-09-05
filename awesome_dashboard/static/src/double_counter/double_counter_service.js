/** @odoo-module **/

import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

const doubleCounterService = {
  start() {
    const state = reactive({ count1: 0, count2: 0 });
    return {
      state,
      increment(counter) {
        state[counter]++;
      },
    };
  },
};

registry.category("services").add("double_counter", doubleCounterService);
