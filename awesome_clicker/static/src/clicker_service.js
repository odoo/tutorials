import {registry} from "@web/core/registry";
import {ClickerModel} from "./clicker_model";
import {browser} from "@web/core/browser/browser";


const clickerService = {
    dependencies: ["effect"],
    start(env, services) {

        const localState = JSON.parse(browser.localStorage.getItem("clickerState"));
        const model = localState ? ClickerModel.fromJSON(localState) : new ClickerModel();


        setInterval(() => {
            model.tick();
        }, 1000);

        setInterval(() => {
            browser.localStorage.setItem("clickerState", JSON.stringify(model));
        }, 10000);

        document.addEventListener("click", () => model.increment(1), true);

        const bus = model.bus;
        bus.addEventListener(
            "milestone_1k", () => {
                services.effect.add({
                    message: "You reached 1000 clicks!",
                    type: "rainbow_man",
                });
            });
        bus.addEventListener(
            "milestone_5k", () => {
                services.effect.add({
                    message: "You reached 5 000 clicks!",
                    type: "rainbow_man",
                });
            });
        bus.addEventListener(
            "milestone_10k", () => {
                services.effect.add({
                    message: "You reached 10 000 clicks!",
                    type: "rainbow_man",
                });
            });

        return model;
    },
};

registry.category("services").add("awesome_clicker.clickerService", clickerService);
