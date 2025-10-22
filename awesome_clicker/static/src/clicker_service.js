import { registry } from "@web/core/registry";
import { ClickerModel } from "./clicker_model";
import { migrate } from "./clicker_migration";

const clickerService = {
    dependencies: ["effect", "notification"],
    start(env, services) {
        const localClicker = migrate(JSON.parse(localStorage.getItem("clicker")))
        const clicker = localClicker ? Object.assign(new ClickerModel(), localClicker) : new ClickerModel()

        setInterval(() => {
            clicker.bots.forEach((bot) => clicker.increment(clicker.power * bot.amount * bot.clicks));
        }, 10*1000);

        setInterval(() => {
            clicker.trees.forEach((tree) => tree.fruit_number += tree.amount)
        }, 30*1000)

        setInterval(() => {
            localStorage.setItem("clicker", JSON.stringify(clicker));
        }, 10*1000);

        const bus = clicker.bus;
        bus.addEventListener("MILESTONE", (ev) => {
            services.effect.add({
                type: "rainbow_man",
                message: `Milestone reached! You can now buy ${ev.detail.unlock}`
            });
        });

        bus.addEventListener("REWARD", (ev) => {
            const reward = ev.detail;
            const closeNotification = services.notification.add(`Congrats you won a reward: "${reward.description}"`,{
                    type: "success",
                    sticky: true,
                    buttons: [
                        {
                            name: "Collect",
                            onClick: () => {
                                reward.apply(clicker);
                                closeNotification();
                            },
                        },
                    ],
                }
            );
        })

        return clicker
    },
};

registry.category("services").add("awesome_clicker.clicker_service", clickerService);
