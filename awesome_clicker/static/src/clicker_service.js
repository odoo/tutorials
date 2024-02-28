/** @odoo-module **/

import { registry } from "@web/core/registry";
import { ClickerModel } from "./clicker_model";

const clickerService = {
    dependencies: ["effect", "action", "notification"],
    start(env, services) {
        const model = new ClickerModel();
        model.bus.addEventListener("MILESTONE_1K", (ev) => {
            services.effect.add({
                message: `Milestone reached! You can now buy ${ev}`,
                type: "rainbow_man",
            });
        });

        model.bus.addEventListener("REWARD", (ev) => {
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
        return model;
    },
};

registry.category("services").add("clickerService", clickerService);
