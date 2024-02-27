/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Clicker } from "./model/clicker_model";

const clickerService = {
  dependencies: ["effect"],
  start: (_, services) => {
    const clicker = new Clicker();
    clicker.eventBus.addEventListener("MILESTONE", (e) =>
      services.effect.add({
        message: `Milestone reached! You can now buy ${e.detail.unlock}`,
      })
    );

    return clicker;
  },
};

registry
  .category("services")
  .add("awesome_clicker.clickerService", clickerService);
