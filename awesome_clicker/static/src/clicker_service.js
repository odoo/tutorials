import { registry } from "@web/core/registry";
import { ClickerModel } from "./clicker_model";

export const clickerService = {
    start() {
        const model = new ClickerModel();

        document.addEventListener("click", () => model.increment(1), true);
        setInterval(() => model.botsDoClicks(10), 10000);
        return model;
    },
};

registry.category("services").add("awesome_clicker.game_service", clickerService);
