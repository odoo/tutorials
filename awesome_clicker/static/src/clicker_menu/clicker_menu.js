import { Component, useExternalListener, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class ClickerMenu extends Component {
    static template = "awesome_clicker.clicker_menu";

    setup() {
        this.state = useState({ value: 0 });
        this.action = useService("action");
        useExternalListener(document.body, "click", () => this.incrementState(this.state, 1));
    }

    incrementState(state, val) {
        state.value += val;
    }

    doAction() {
        this.action.doAction({
            type: "ir.actions.client",
            tag: "awesome_clicker.clicker_action",
            target: "new",
            name: "Clicker Game",
        });
    }
}

export const systrayItem = {
    Component: ClickerMenu,
};

registry.category("systray").add("awesome_clicker.clicker_menu", systrayItem);
