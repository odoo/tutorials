/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useClicker } from "../use_clicker";
import { useService } from "@web/core/utils/hooks";
import { ClickValue } from "../click_value/click_value";


class ClickerSystrayItem extends Component {
    static template = "awesome_clicker.ClickerSystrayItem";
    static components = {ClickValue};
    static props = []

    setup() {
        this.action = useService("action");
        this.clicker = useClicker();
    }

    onClick() {
        this.clicker.increment(1);
    }

    openAction() {
        this.action.doAction({
            type: "ir.actions.client",
            tag: "awesome_clicker.client_action",
            target: "new",
            name: "Clicker"
        });
    }
}



registry.category("systray").add("awesome_clicker.ClickerSystrayItem", {
    Component: ClickerSystrayItem
});