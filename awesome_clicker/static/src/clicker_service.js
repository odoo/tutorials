import { useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

import { ClickerModel, LEVEL_REQUIREMENTS } from "./clicker_model";


const clickerService = {
    dependencies: ["action", "effect", "notification"],
    start(env, services) {
        let clicker_model = new ClickerModel();

        LEVEL_REQUIREMENTS.forEach(milestone =>
            clicker_model.bus.addEventListener(
                milestone.event_name,
                () => services.effect.add({ message: milestone.message }),
            )
        )

        clicker_model.bus.addEventListener(
            "RANDOM_REWARD",
            (ev) => {
                const closeNotification = services.notification.add(
                    `Congratulations, you won a reward: '${ev.detail.description}'`,
                    {
                        type: "success",
                        sticky: true,
                        buttons: [{
                            name: "Collect",
                            onClick: () => {
                                ev.detail.apply(clicker_model);
                                closeNotification();
                                services.action.doAction({
                                    type: "ir.actions.client",
                                    tag: "awesome_clicker.client_action",
                                    target: "new",
                                    name: "Clicker"
                                });
                            }
                        }],
                    }
                )
            }
        )

        return clicker_model;
    }
}

export function useClicker() {
    return useState(useService("awesome_clicker.clicker_service"));
}

registry.category("services").add("awesome_clicker.clicker_service", clickerService);
