import { registry } from "@web/core/registry";
import { ClickerModel } from "./model/clicker_model";

export const getCount = {
    dependencies: ["effect"],
    start(env, services) {
        const clicker = new ClickerModel();

        setInterval(() => {
            clicker.tick();
        }, 10000)

        const bus = clicker.bus
        bus.addEventListener("MILESTONE", (ev) => {
            services.effect.add({
                message: `Milestone reached! You can now buy ${ev.detail}!`,
                type: "rainbow_man",
            })
        })

        document.addEventListener("click", () => clicker.increment(1), true)

        return clicker;
    }
}

registry.category("services").add("awesome_clicker.count", getCount);
