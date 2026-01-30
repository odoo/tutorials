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
            },

            // Commands below are strictly for debugging, they are not part of the tutorial exercises
            {
                name: "Increment Clicker by 1,000",
                category: "debug",
                action() {
                    env.services["awesome_clicker.clicker_service"].increment(1000);
                }
            },
            {
                name: "Increment Clicker by 100,000",
                category: "debug",
                action() {
                    env.services["awesome_clicker.clicker_service"].increment(100000);
                }
            },
            {
                name: "Increment Clicker by 1,000,000",
                category: "debug",
                action() {
                    env.services["awesome_clicker.clicker_service"].increment(1000000);
                }
            },
            {
                name: "Grant Clicker Reward",
                category: "debug",
                action() {
                    env.services["awesome_clicker.clicker_service"].getReward();
                }
            },
            {
                name: "Reset Clicker Game",
                category: "debug",
                action() {
                    let clicker = env.services["awesome_clicker.clicker_service"];
                    Object.values(clicker.bots).forEach(bot => bot.quantity = 0);
                    clicker.power = 1;
                    clicker.level = 0;
                    clicker.clicks = 0;
                }
            },
        ]}
    }
);
