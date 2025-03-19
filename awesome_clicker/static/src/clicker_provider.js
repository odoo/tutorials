/* @odoo-module */
import { registry } from "@web/core/registry";


const clickerProviderRegistry = registry.category("command_provider");

clickerProviderRegistry.add("clicker", {
    provide: (env, options) => {
        return [
            {
                action(){
                    env.services["clickerService"].buyBot(1);
                },
                category: "clicker",
                name: "Buy 1 click bot"
            },
            {
                action(){
                    env.services.action.doAction({
                        type: "ir.actions.client",
                        tag: "awesome_clicker.client_action",
                        target: "new",
                        name: "Clicker Game"
                    });
                },
                category: "clicker",
                name: "Open Clicker Game"
            },
        ]
    }
});
