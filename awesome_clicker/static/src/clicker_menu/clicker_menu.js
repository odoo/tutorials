import { Component, useExternalListener, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class ClickerMenu extends Component {
    static template = "awesome_clicker.clicker_menu";

    setup() {
        this.state = useState({ value: 0 });
        useExternalListener(document.body, "click", () => this.incrementState(this.state, 1));
    }

    incrementState(state, val) {
        state.value += val;
    }
}

export const systrayItem = {
    Component: ClickerMenu,
};

registry.category("systray").add("awesome_clicker.clicker_menu", systrayItem);
