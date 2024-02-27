/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Clicker } from "./model/clicker_model";

const clickerService = {
  dependencies: ["effect", "action", "notification"],
  start: (_, services) => {
    const clicker = new Clicker();
    clicker.eventBus.addEventListener("MILESTONE", (e) =>
      services.effect.add({
        message: `Milestone reached! You can now buy ${e.detail.unlock}`,
      })
    );
    clicker.eventBus.addEventListener("REWARD", (e) => {
      const reward = e.detail;
      const notification = services.notification.add(
        `Congrats you won a reward: "${reward.description}"`,
        {
          type: "success",
          sticky: true,
          buttons: [
            {
              name: "Collect",
              onClick: () => {
                reward.apply(clicker);
                notification();
                services.action.doAction({
                  type: "ir.actions.client",
                  tag: "awesome_clicker.client_action",
                  target: "new",
                  name: "Clicker Game",
                });
              },
            },
          ],
        }
      );
    });

    return clicker;
  },
};

registry
  .category("services")
  .add("awesome_clicker.clickerService", clickerService);
