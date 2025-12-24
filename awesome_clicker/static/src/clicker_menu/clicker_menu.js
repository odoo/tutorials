import { Component, useExternalListener } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { useClicker } from "../utils";

export class ClickerMenu extends Component {
    static template = "awesome_clicker.clicker_menu";

    setup() {
        this.clicker = useClicker();
        useExternalListener(document.body, "click", () => this.clicker.increment(1));
        this.action = useService("action");
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
