/** @odoo-module **/

import { Component, useState, useExternalListener } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { useClicker } from "./clicker_hook";
import { ClickerValue } from "./clicker_value";

export class ClickerSystray extends Component {
    static template = "awesome_clicker.clicker_systray";
    static props = {};
    static components = { ClickerValue };

    setup() {
        this.clickerHook = useClicker();
        this.action = useService("action");
    }

    open_client_action() {
        this.action.doAction({
            type: "ir.actions.client",
            tag: "awesome_clicker.client_action",
            target: "new",
            name: "Clicker"
        });
    }
}

export const systrayItem = {
    Component: ClickerSystray,
};

registry.category("systray").add("awesome_clicker.clicker_systray", systrayItem, { sequence: 23 });
