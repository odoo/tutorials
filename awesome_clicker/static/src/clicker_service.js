import { registry } from "@web/core/registry";
import { ClickerModel } from "./clicker_model";
import { BOT_FREQUENCY, MILESTONES } from "./clicker_data";

export const clickerService = {
    dependencies: ["effect"],
    start(env, deps) {
        const model = new ClickerModel();

        for (const milestone of MILESTONES) {
            model.bus.addEventListener(milestone.event, () =>
                deps.effect.add({ message: `Milestone reached! ${milestone.description}` })
            );
        }
        document.addEventListener("click", () => model.increment(1), true);
        setInterval(() => model.botsDoClicks(), BOT_FREQUENCY);
        return model;
    },
};

registry.category("services").add("awesome_clicker.game_service", clickerService);
