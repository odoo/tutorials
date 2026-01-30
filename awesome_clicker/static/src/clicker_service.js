import { useState } from "@odoo/owl";
import { browser } from "@web/core/browser/browser";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

import { ClickerModel, LEVEL_REQUIREMENTS } from "./clicker_model";
import { migrate } from "./migration";


function initClickerState() {
    let clicker_model = new ClickerModel();
    let local_state = JSON.parse(browser.localStorage.getItem("clicker_state"));

    if (!local_state) {
        return clicker_model;
    }

    if (local_state.version != clicker_model.version) {
        migrate(local_state, clicker_model.version);
    }

    delete local_state.bus;
    return Object.assign(clicker_model, local_state);
}

const clickerService = {
    dependencies: ["action", "effect", "notification"],
    start(env, services) {
        let clicker_model = initClickerState();

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
