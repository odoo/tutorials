import { registry } from "@web/core/registry";

const commandProviderRegistry = registry.category("command_provider");

commandProviderRegistry.add("clicker", {
    provide: (env, options) => {
        return [
            {
                name: "Open Clicker Game",
                action() {
                    env.services.action.doAction({
                        type: "ir.actions.client",
                        tag: "awesome_clicker.client_action",
                        target: "new",
                        name: "Clicker Game",
                    });

                },
            },
            {
                name: "Buy one ClickBot",
                action() {
                    env.services["awesome_clicker.clicker_service"].buyBot("clickbot");
                    env.services.action.doAction({
                        type: "ir.actions.client",
                        tag: "awesome_clicker.client_action",
                        target: "new",
                        name: "Clicker Game",
                    });
                }
            }
        ];
    },
});
    