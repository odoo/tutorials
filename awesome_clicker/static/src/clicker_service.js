import { registry } from "@web/core/registry";
import { ClickerModel } from "./clicker_model";

const clickerService = {
    start(env) {
        const model = new ClickerModel();

        document.addEventListener("click", () => model.addClick(), true);
        setInterval(() => {
            model.tick();
        }, 10000);

        return model;
    },
};

registry.category("services").add("awesome_clicker.clicker", clickerService);
