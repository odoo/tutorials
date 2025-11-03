import { registry } from "@web/core/registry";
import { ClickerModel } from "./clicker_model";
import { browser } from "@web/core/browser/browser";
import { migrate } from "./clicker_migration";

const clickerService = {
    dependencies: ["action", "effect", "notification"],
    start(env, services) {
        const localState = migrate(JSON.parse(browser.localStorage.getItem("clickerState")));
        const model = localState ? ClickerModel.fromJSON(localState): new ClickerModel();

        document.addEventListener("click", () => model.increment(1), true);

        setInterval(() => model.clickBotsAction(), 10000);
        setInterval(() => model.treesAction(), 30000);
        setInterval(() => {
            browser.localStorage.setItem("clickerState", JSON.stringify(model))
        }, 10000);

        const bus = model.bus;
        bus.addEventListener("MILESTONE", (ev) => {
            services.effect.add({
                message: `Milestone reached! You can now buy ${ev.detail.bot}`,
                type: "rainbow_man",
            });
        });

        bus.addEventListener("REWARD", (ev) => {
            const closeNotification = services.notification.add(
                `Congrats you won a reward: "${ev.detail.description}"`,
                {
                    type: "success",
                    sticky: true,
                    buttons: [
                        {
                            name: "Collect",
                            onClick: () => {
                                ev.detail.apply(model);
                                closeNotification();
                                services.action.doAction({
                                    type: "ir.actions.client",
                                    tag: "awesome_clicker.ClientAction",
                                    target: "new",
                                    name: "Clicker Game"
                                });
                            },
                        },
                    ],
                }
            );
        });

        return model
    }
}

registry.category("services").add("awesome_clicker.clicker", clickerService);
