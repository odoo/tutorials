/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class ClickerSystrayItem extends Component {
    static template = "awesome_clicker.ClickerSystrayItem"

    setup() {
        this.action = useService("action");
        this.clickerService  = useState(useService('clicker_service'))
    }

    incrementScore() {
        this.clickerService.incrementScore(9)
    }

    openClientAction() {
        this.action.doAction({
            type: "ir.actions.client",
            tag: "awesome_clicker.client_action",
            target: "new",
            name: "Clicker Game",
        });
    }
}

registry.category("systray").add("awesome_clicker.ClickerSystrayItem", {
    Component: ClickerSystrayItem,
});