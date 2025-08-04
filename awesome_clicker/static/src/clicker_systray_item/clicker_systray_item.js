/** @odoo-module **/

import { Component, useExternalListener } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { useClicker } from "../clicker_hook";
import { ClickerValue } from "../clicker_value/clicker_value";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";

// HelloWorld OWL component
export class ClickerSystray extends Component {
    static template = "awesome_clicker.ClickerSystray";
    static components = { ClickerValue, Dropdown, DropdownItem };

    setup() {
        this.action = useService("action");
        this.clicker = useClicker()
        useExternalListener(document.body, "click", this.randomClick, { capture: true });
    }

    openClientAction() {
        this.action.doAction({
            type: "ir.actions.client",
            tag: "awesome_clicker.client_action",
            target: "new",
            name: "Clicker"
        });
    }

    sisTrayClick() {
        this.clicker.increment(9);
    }

    randomClick() {
        this.clicker.increment(1);
    }

    get nTrees() {
        return this.clicker.cherryTree + this.clicker.pearTree;
    }

    get nFruits() {
        return this.clicker.cherries + this.clicker.pears;
    }
}

export const systrayItem = {
    Component: ClickerSystray,
};

registry.category("systray").add("awesome_clicker.ClickerSystray", systrayItem);
