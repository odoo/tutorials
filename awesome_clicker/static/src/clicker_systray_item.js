/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useExternalListener } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { useClicker } from "./clicker_hook";
import { ClickerValue } from "./clicker_value";

class ClickerSystray extends Component {
    static template = "awesome_clicker.ClickerSystray";
    static components = { ClickerValue };

    setup() {
        this.action = useService("action");
        this.clicker_hook = useClicker();
        useExternalListener(document.body, "mousedown", () => this.clicker_hook.increment(1), {capture:true});
    }

    displayClickerPanel() {
        this.action.doAction({
            type: "ir.actions.client",
            tag: "awesome_clicker.client_action",
            target:"new",
            name: "Clicker Game"
        });
    }
}

registry.category("systray").add("awesome_clicker.ClickerSystray", {
    Component: ClickerSystray,
});
