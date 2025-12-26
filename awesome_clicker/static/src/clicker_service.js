import { registry } from "@web/core/registry";
import { ClickerModel } from "./clicker_model";
import { BOT_FREQUENCY, MILESTONES, TREE_FREQUENCY } from "./clicker_data";
import { browser } from "@web/core/browser/browser";

export function doClickerAction(actionService) {
    actionService.doAction({
        type: "ir.actions.client",
        tag: "awesome_clicker.clicker_action",
        target: "new",
        name: "Clicker Game",
    });
}

export const clickerService = {
    dependencies: ["effect", "action", "notification"],
    start(env, { effect, action, notification }) {
        const model = new ClickerModel();
        const persistentState = browser.localStorage.getItem("clicker_state");
        if (persistentState) {
            model.persistentState = JSON.parse(persistentState);
        }

        for (const milestone of MILESTONES) {
            model.bus.addEventListener(milestone.event, () =>
                effect.add({ message: `Milestone reached! ${milestone.description}` })
            );
        }

        model.bus.addEventListener("REWARD", (ev) => {
            const closeNotif = notification.add(
                `You've earned a reward: ${ev.detail.description}`,
                {
                    title: "Clicker Reward",
                    type: "success",
                    sticky: true,
                    buttons: [
                        {
                            name: "Collect",
                            onClick: () => {
                                closeNotif();
                                ev.detail.apply(model);
                                doClickerAction(action);
                            },
                        },
                    ],
                }
            );
        });

        document.addEventListener("click", () => model.increment(1), true);
        setInterval(() => model.botsDoClicks(), BOT_FREQUENCY);
        setInterval(() => model.treesProduceFruit(), TREE_FREQUENCY);
        setInterval(
            () =>
                browser.localStorage.setItem(
                    "clicker_state",
                    JSON.stringify(model.persistentState)
                ),
            10000
        );
        return model;
    },
};

registry.category("services").add("awesome_clicker.game_service", clickerService);
