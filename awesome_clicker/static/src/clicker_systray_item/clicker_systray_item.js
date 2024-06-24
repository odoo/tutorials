/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, useExternalListener } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks"


class ClickerSystrayItem extends Component {
    static template = "awesome_clicker.ClickerSystrayItem";

    setup() {
        this.state = useState({ click_count: 0 });

        useExternalListener(window, "click", this.incrementCounter, { capture: true });
        this.actionService = useService("action");
    }

    incrementCounter(){
        this.state.click_count++;
    }

    incrementButtonAction() {
        this.state.click_count += 9;
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