import { registry } from "@web/core/registry";
import { ClickerModel } from "./clicker_model";

export const clickerService = {
    dependencies: ["effect"],
    start(env, deps) {
        const model = new ClickerModel();

        model.bus.addEventListener("MILESTONE_1k", () =>
            deps.effect.add({ message: "Milestone reached! You can now buy clickbots." })
        );
        document.addEventListener("click", () => model.increment(1), true);
        setInterval(() => model.botsDoClicks(10), 10000);
        return model;
    },
};

registry.category("services").add("awesome_clicker.game_service", clickerService);
