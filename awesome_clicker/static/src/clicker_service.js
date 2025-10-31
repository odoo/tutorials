import { registry } from "@web/core/registry";
import { ClickerModel } from "./clicker_model";

const ClickerService = {
    dependencies: ["effect", "action", "notification"],
    start(env, services) {
        const clicker = new ClickerModel()

        document.addEventListener("click", () => clicker.increment(1), true);
        clicker.bus.addEventListener("Level1", () => services.effect.add({ message: "Level up! You can now buy click bots!"}))
        clicker.bus.addEventListener("Level2", () => services.effect.add({ message: "Level up! You can now buy big bots!"}))
        clicker.bus.addEventListener("Level3", () => services.effect.add({ message: "Level up! You can now buy powers!"}))
        clicker.bus.addEventListener("Reward", (e) => {
            const reward = e.detail;
            const closeNotification = services.notification.add(`You won a reward!: "${reward.description}"`,
                {
                    type: "success",
                    sticky: true,
                    buttons: [
                        {
                            name: "Collect",
                            onClick: () => {
                                reward.apply(clicker);
                                closeNotification();
                                services.action.doAction({
                                    type: "ir.actions.client",
                                    tag: "awesome_clicker.client_action",
                                    target: "new",
                                    name: "Clicker Game"
                                })
                            }
                        }
                    ]
                })
        })

        setInterval(() => clicker.tick(), 10 * 1000)
        return clicker;
    },
};

registry.category("services").add("clicker", ClickerService);