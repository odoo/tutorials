import { registry } from "@web/core/registry";


registry.category("command_provider").add(
    "clicker_game", {
        provide: (env, options) => { return [
            {
                name: "Open Clicker Game",
                category: "activity",
                action() {
                    env.services.action.doAction({
                        type: "ir.actions.client",
                        tag: "awesome_clicker.client_action",
                        target: "new",
                        name: "Clicker"
                    });
                }
            },
            {
                name: "Buy 1 ClickBot",
                category: "activity",
                action() {
                    env.services["awesome_clicker.clicker_service"].purchaseBot("ClickBot");
                }
            }
        ]}
    }
);
