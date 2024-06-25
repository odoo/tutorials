/** @odoo-module **/

import { registry } from "@web/core/registry";
import { ClickerModel } from "./clicker_model";


const clickerService = {
    dependencies: ['effect', 'notification', 'action'],
    start(env, services) {

        const clicker_model = new ClickerModel();
        clicker_model.bus.addEventListener("MILESTONE_REACHED", (event) => {
            services.effect.add({message: `You have reached level ${event.detail}!`}
        )});

        clicker_model.bus.addEventListener("REWARD_RECEIVED", (ev) => {
            const reward = ev.detail;
            const closeNotification = services.notification.add(
                `Congrats you won a reward: "${reward.description}"`,
                {
                    type: "success",
                    sticky: true,
                    buttons: [
                        {
                            name: "Collect",
                            onClick: () => {
                                reward.apply(clicker_model);
                                closeNotification();
                                services.action.doAction({
                                    type: "ir.actions.client",
                                    tag: "awesome_clicker.client_action",
                                    target: "new",
                                    name: "Clicker Game"
                                });
                            },
                        },
                    ],
                }
            );
        })

        return clicker_model;
    }
}

registry.category("services").add("awesome_clicker.clickCounter", clickerService);
