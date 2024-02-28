/** @odoo-module */

import { registry } from "@web/core/registry";
import { ClickerModel } from "./clicker_model";

const ClickerService = {
    dependencies: ["action", "effect", "notification"],
    start(env, services) { 
        const clickerModel = new ClickerModel();

        const bus = clickerModel.bus;

        bus.addEventListener("MILESTONE", (ev) => {
            services.effect.add({
                message: `Milestone reached! You can now buy ${ev.detail.unlock}`,
            })
        })

        bus.addEventListener("REWARD", (ev) => {
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
                                reward.apply(clickerModel);
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

        return clickerModel;
    },
};

registry.category("services").add("awesome_clicker.clicker", ClickerService);
