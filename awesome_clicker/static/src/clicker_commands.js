import { registry } from "@web/core/registry";
import { doClickerAction } from "./clicker_service";

const commandRegistry = registry.category("command_provider");

commandRegistry.add("clicker", {
    provide: (env, options) => [
        {
            name: "Open Clicker Game",
            action: () => doClickerAction(env.services.action),
        },
        {
            name: "Buy 1 click bot",
            action: () => {
                env.services["awesome_clicker.game_service"].purchase("clickbot");
            },
        },
    ],
});
