/** @odoo-module */

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

import { Component } from "@odoo/owl";

import { useClicker } from "./use_clicker";
import { ClickValue } from "./click_value";

export class ClickerSystray extends Component {
    static template = "awesome_clicker.ClickerSystray";
    static components = { ClickValue };
    static props = {};

    setup() {
        this.clicker = useClicker();
        this.action = useService("action");
    }

    openClientAction() {
        this.action.doAction({
            type: "ir.actions.client",
            tag: "awesome_clicker.client_action",
            target: "new",
            name: "Clicker"
        })
    }
}

registry.category("systray").add(
    "awesome_clicker.clicker_systray",
    {
        Component: ClickerSystray
    },
    {
        sequence: 100
    }
);

