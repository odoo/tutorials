import { registry } from "@web/core/registry";
import { Clicker } from "./clicker_model";

export const clickerService = {
    dependencies: ["effect"],
    start(env, services) {
        const clicker = new Clicker();
        clicker.bus.addEventListener("MILESTONE_1k", () => {
            services.effect.add({ message: "Boom! You reached 1k milestone. You can now buy bots!", });
        });
        clicker.bus.addEventListener("MILESTONE_5k", () => {
            services.effect.add({ message: "Boom! You reached 5k milestone. You can now buy big bots!", });
        });
        clicker.bus.addEventListener("MILESTONE_100k", () => {
            services.effect.add({ message: "Boom! You reached 100k milestone. You can now buy power!", });
        });
        clicker.bus.addEventListener("MILESTONE_1M", () => {
            services.effect.add({ message: "Boom! You reached 1M milestone. You can now buy trees!", });
        });
        return clicker;
    }
};

registry.category("services").add("awesome_clicker_service", clickerService);
