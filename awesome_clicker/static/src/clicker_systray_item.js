
import { Component, useExternalListener, useState } from "@odoo/owl";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";


export class systrayCounter extends Component {

    static template = "awesome_clicker.systrayCounter";
    static components = { Dropdown, DropdownItem };
    static props = {};

    setup() {
        this.action = useService("action");
        this.clicker = useState(useService("awesome_clicker_service"))
        useExternalListener(window, "click", this.onClickWindow, { capture: true });

        registry.category("command_provider").add("clicker", {
            provide(env, options) {
                const commands = [];
                if (env.services.awesome_clicker_service.clicks >= 1000) {
                    commands.push({
                        action() {
                            env.services.awesome_clicker_service.buyBot();
                        },
                        category: "clicker",
                        name: "Buy 1 click bot",
                    })
                }
                commands.push({
                    action() {
                        env.services.action.doAction({
                            type: "ir.actions.client",
                            tag: "awesome_clicker.client_action",
                            target: "new",
                            name: "Clicker"
                        });
                    },
                    category: "clicker",
                    name: "Open Clicker Game",
                });
                return commands;
            }
        });
    }

    onClickWindow() {
        this.clicker.increment(1);
    }

    openClient() {
        this.action.doAction({
            type: "ir.actions.client",
            tag: "awesome_clicker.client_action",
            target: "new",
            name: "Clicker"
        });
    }
};

export const systrayItem = {
    Component: systrayCounter,
};

registry.category("systray").add("clicker_menu", systrayItem);
