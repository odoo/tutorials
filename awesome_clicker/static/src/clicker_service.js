/** @odoo-module **/

import { browser } from "@web/core/browser/browser";
import { registry } from "@web/core/registry";
import { migrate } from "./clicker_migration";
import { ClickerModel } from "./clicker_model";

const clickerService = {
    dependencies: ["action", "effect", "notification"],
    start(env, services) {
        const localState = migrate(JSON.parse(browser.localStorage.getItem("clickerState")));
        const model = localState ? ClickerModel.fromJSON(localState): new ClickerModel();

        setInterval(() => {
            browser.localStorage.setItem("clickerState", JSON.stringify(model))
        }, 10000);

        const bus = model.bus;
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
                                reward.apply(model);
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
        });

        bus.addEventListener("MILESTONE_1K", () => {
            services.effect.add({
                message: `Milestone reached!`,
                type: "rainbow_man",
            });
        });

        return model;
    },
};

registry.category("services").add("awesome_clicker.clicker", clickerService);
