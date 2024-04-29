/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useExternalListener, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class ClickerSystrayItem extends Component {
    static template = "awesome_clicker.ClickerSystrayItem"

    setup() {
        this.action = useService("action");
        this.state = useState({ score: 0 })
        useExternalListener(document.body, "click", () => this.state.score++, { capture: true });
    }

    incrementScore() {
        this.state.score += 9;
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