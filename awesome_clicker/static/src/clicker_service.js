import { registry } from "@web/core/registry";
import { ClickerModel } from "./clicker_model";

export const clickerService = {
    dependencies: ["effect"],
    start(env, deps) {
        const MILESTONE_MESSAGES = {
            MILESTONE_1k: "Milestone reached! You can now buy clickbots.",
            MILESTONE_5k: "Milestone reached! You can now buy bigbots.",
            MILESTONE_100k: "Milestone reached! You can now increase your power level.",
        };

        const model = new ClickerModel();

        for (const [key, value] of Object.entries(MILESTONE_MESSAGES)) {
            model.bus.addEventListener(key, () => deps.effect.add({ message: value }));
        }
        document.addEventListener("click", () => model.increment(1), true);
        setInterval(() => model.botsDoClicks(), 10000);
        return model;
    },
};

registry.category("services").add("awesome_clicker.game_service", clickerService);
