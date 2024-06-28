/** @odoo-module **/

import { registry } from "@web/core/registry";

const commandProviderRegistry = registry.category("command_provider");

commandProviderRegistry.add("clicker", {
    provide: (env, options) => {
        return [
            {
                name: "Buy 1 click bot",
                action() {
                    env.services["awesome_clicker.clicker"].buy("clickBots", 1000);
                },
            },
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
        ];
    },
});