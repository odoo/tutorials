import { registry } from "@web/core/registry";
import { useClicker } from "../clicker_hook/clicker_hook";

registry.category("command_provider").add("clicker", {provide: (env,options) => 
    {
        return [
            {
                name:"Open Clicker Menu",
                action()
                {
                    env.services.action.doAction({
                            type: "ir.actions.client",
                            tag: "awesome_clicker.client_action",
                            target: "new",
                            name: "Clicker"
                        });
                }
            },
            {
                name:"Add Bot",
                action()
                {
                    env.services["awesome_clicker.clicker_service"].bots.clickBot.quantity ++;
                }
            },
            {
                name:"Add Big Bot",
                action()
                {
                    env.services["awesome_clicker.clicker_service"].bots.bigClickBot.quantity ++;
                }
            },
            {
                name:"Add Many Big Bot",
                action()
                {
                    env.services["awesome_clicker.clicker_service"].bots.bigClickBot.quantity += 500;
                }
            }
        ]
    }
})
