/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, useExternalListener } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";


class ClickerSystrayItem extends Component {
    static template = "awesome_clicker.ClickerSystrayItem";
    static props = {
        description: { type: String, optional: true }
    };

    setup() {
        this.clickerService = useState(useService("awesome_clicker.clickCounter"));

        useExternalListener(window, "click", this.incrementCounter, { capture: true });
        this.actionService = useService("action");
    }

    incrementCounter(){
        this.clickerService.increment(1);
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