/** @odoo-module **/

import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

const clickerService = {
  dependencies: [],
  start() {
    const state = reactive({ count: 0 });

    document.addEventListener("click", () => state.count++, true);

    return {
      state,
      increment(inc) {
        state.count += inc;
      },
    };
  },
};

registry
  .category("services")
  .add("awesome_clicker.clickerService", clickerService);
