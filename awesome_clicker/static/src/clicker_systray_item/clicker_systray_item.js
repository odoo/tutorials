/** @odoo-module **/

import { Component, useExternalListener } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { useClicker } from "../useClicker";
import { ClickValue } from "../click_value/click_value";
import { Dropdown } from "@web/core/dropdown/dropdown";

export class ClickerSystrayItem extends Component {
    static template = "awesome_owl.ClickerSystrayItem";
    
    static components = { ClickValue, Dropdown }

    setup() {
        this.action = useService("action");
        this.clicker = useClicker();
        useExternalListener(window, "click", () => this.clicker.increment(1), { capture: true });
    }

    openClientAction() {
        this.action.doAction({
            type: "ir.actions.client",
            tag: "awesome_clicker.client_action",
            target: "new",
            name: "Clicker"
        });
    }
}

registry.category("systray").add("awesome_owl.ClickerSystrayItem", {
    Component: ClickerSystrayItem,
});