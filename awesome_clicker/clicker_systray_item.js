/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, useExternalListener } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class ClickerSystray extends Component {
    static template = "awesome_clicker.ClickerSystray";

    setup() {
        this.clicks = useState({ value: 0 });
        this.action = useService("action");
        this.increment = this.incrementClicks.bind(this);
        useExternalListener(document.body, "mousedown", () => this.increment(1));
    }

    incrementClicks(val) {
        this.clicks.value += val;
    }

    displayClickerPanel() {
        console.log("jngfcghj");
        this.action.doAction({
            type: "ir.actions.client",
            tag: "awesome_clicker.client_action",
            target:"new",
            name: "Clicker"
        });
    }
}

registry.category("systray").add("awesome_clicker.ClickerSystray", {
    Component: ClickerSystray,
});
