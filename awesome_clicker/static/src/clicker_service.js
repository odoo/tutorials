import { registry } from "@web/core/registry";
import { ClickerModel } from "./clicker_model";

const clickerService = {
    dependencies: ["action", "effect", "notification"],
    start(env, services) {
        const model = new ClickerModel();

        document.addEventListener("click", () => model.addClick(), true);
        setInterval(() => {
            model.tick();
        }, 10000);
        const bus = model.bus;
        bus.addEventListener("MILESTONE", (ev) => {
            services.effect.add({
                message: `Milestone reached! You can now buy ${ev.detail.unlock}`,
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
        })
        return model;
    },
};

registry.category("services").add("awesome_clicker.clicker", clickerService);
