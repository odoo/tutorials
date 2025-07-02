/** @odoo-module **/
import { registry } from "@web/core/registry";
import { ClickerModel } from "./models/clicker_model";
import { browser } from "@web/core/browser/browser";
import { migrate } from "./clicker_migration";

export const clickerService = {
    dependencies: ["action", "effect", "notification"],

    start(env, services) {
        const localState = migrate(JSON.parse(browser.localStorage.getItem("clickerState")));
        const clickerModel = localState ? ClickerModel.fromJSON(localState) : new ClickerModel();
        setInterval(() => {
            browser.localStorage.setItem("clickerState", JSON.stringify(clickerModel))
        }, 10000);

        const bus = clickerModel.bus;
        bus.addEventListener("MILESTONE_1k", () => {
            services.effect.add({
                message: "Milestone reached! You can now buy clickbots",
                type: "rainbow_man",
            });
        });
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
                                    tag: "clicker_client_action.ClickerClientAction",
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
    }
}
registry.category("services").add("clicker", clickerService);
