/** @odoo-module **/

import { registry } from "@web/core/registry";
import { ClickerModel } from "./clicker_model";
import { browser } from "@web/core/browser/browser";

import { migrate } from "./clicker_migrations.js";


const clickerService = {
    dependencies: ['effect', 'notification', 'action'],
    start(env, services) {

        const localState = migrate(JSON.parse(browser.localStorage.getItem("clickerState")) );
        const clicker_model = localState ? ClickerModel.fromJSON(localState) : new ClickerModel();
        
        setInterval(() => {
            browser.localStorage.setItem("clickerState", JSON.stringify(clicker_model))
        }, 10000);

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
