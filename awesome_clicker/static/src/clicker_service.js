import { registry } from "@web/core/registry";
import { ClickerModel } from "./clicker_model";
import { EventBus } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { browser } from "@web/core/browser/browser";


const clickerService = {
    dependencies: ["action", "effect", "notification"],
    start(env, services){
        const clicker_state_storage = browser.localStorage.getItem("clicker_state");
        let state = undefined;
        if(clicker_state_storage){
            state = JSON.parse(clicker_state_storage);
        }
        const clicker_model = new ClickerModel(state);

        const bus = clicker_model.bus;
        bus.addEventListener("MILESTONE", (ev) => {
            services.effect.add({
                type: "rainbow_man",
                message: `Milestone reached! You can now buy ${ev.detail.unlock}`,
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
                                reward.apply(clicker_model);
                                closeNotification();
                                services.action.doAction({
                                    type: "ir.actions.client",
                                    tag: "awesome_clicker.client_action",
                                    target: "new",
                                    name: "Clicker Game"
                                });
                            }
                        }
                    ]
                }
            );
        });

        document.addEventListener("click", () => clicker_model.increment(1), true);
        setInterval(() => {
            clicker_model.tick();
            browser.localStorage.setItem("clicker_state", JSON.stringify(clicker_model));
        }, 10000);


        return clicker_model;
    }
};

registry.category("services").add("clickerService", clickerService);
