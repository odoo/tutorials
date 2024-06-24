/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useExternalListener } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

import { useClicker } from "../clicker_hook.js"
import { ClickerValue } from "../clicker_value/clicker_value.js"


class ClickerSystrayItem extends Component {
    static template = "awesome_clicker.ClickerSystrayItem";
    static props = {
        description: { type: String, optional: true }
    };
    static components = { ClickerValue };

    setup() {
        this.clicker = useClicker();

        useExternalListener(window, "click", () => this.clicker.increment(1), { capture: true });
        this.actionService = useService("action");
    }

    openClickerGame() {
        this.actionService.doAction({
            type: "ir.actions.client",
            tag: "awesome_clicker.client_action",
            target: "new",
            name: "Clicker"
         });
    }
}

registry.category("systray").add("awesome_clicker.ClickerSystrayItem", {
    Component: ClickerSystrayItem, isDisplayed: (env) => true
});