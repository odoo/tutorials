import { registry } from "@web/core/registry";

registry.category('command_provider').add("clicker", {
    provide: (env, options) => {
        return [{
                action() {
                    env.services.action.doAction({
                        type: "ir.actions.client",
                        tag: "awesome_clicker.client_action",
                        target: "new",
                        name: "Clicker Game"
                    })
                },
                category: "debug",
                name: "Open clicker game",
            },
            {
                action() {
                    env.services["clicker"].buyClickBot()
                },
                category: "debug",
                name: "Buy one click bot",
            }
        ]
    }
})