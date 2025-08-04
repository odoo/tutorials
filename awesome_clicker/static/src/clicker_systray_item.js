/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useExternalListener } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { useClicker } from "./clicker_service";
import { ClickValue } from "./click_value";

export class ClickerSystrayItem extends Component {
    static template = "awesome_clicker.SystrayItem";
    static components = { ClickValue };
    static props = {};

    setup() {
        this.clicker = useClicker();

        this.action = useService("action");
        useExternalListener(document.body, "click", this.onBodyClick.bind(this));
    }

    onBodyClick() {
        this.clicker.increment(1);
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

const systrayItem = {
    Component: ClickerSystrayItem,
};

registry.category("systray").add("awesome_clicker.SystrayItem", systrayItem, { sequence: 1 });
