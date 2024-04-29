/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useExternalListener, useState } from "@odoo/owl";

class ClickerSystrayItem extends Component {
    static template = "awesome_clicker.ClickerSystrayItem"

    setup() {
        this.state = useState({ score: 0 })
        useExternalListener(document.body, "click", () => this.state.score++, { capture: true });
    }

    incrementScore() {
        this.state.score += 9;
    }
}

registry.category("systray").add("awesome_clicker.ClickerSystrayItem", {
    Component: ClickerSystrayItem,
});