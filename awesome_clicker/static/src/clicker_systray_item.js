/** @odoo-module **/

import { Component, useExternalListener } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks"
import { useClicker } from "./clicker_hook";
import { ClickValue } from "./click_value";

export class ClickerSystrayItem extends Component {
    static template = "awesome_clicker.clicker_systray_item";

    static components = { ClickValue }

    setup() {
        this.clicker = useClicker();
        useExternalListener(document.body, "click", () => this.clicker.increment(1), { capture: true });
        this.action = useService("action")
    }

    openClient() {
        this.action.doAction({
        type: "ir.actions.client",
        tag: "awesome_clicker.client_action",
        target: "new",
        name: "Clicker Game"
        })
    }
}

export const systrayItem = {
    Component: ClickerSystrayItem,
};

registry.category("systray").add("awesome_clicker.clicker_systray_item", systrayItem, { sequence: 1000 })
