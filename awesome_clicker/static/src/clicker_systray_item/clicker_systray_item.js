import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { useClicker } from "../useClicker";
import { ClickerValue } from "../clicker_value";

export class ClickerSystray extends Component {
    static template = "awesome_clicker.ClickerSystray";
    static props = {};

    static components = { ClickerValue };

    document_click = 1;
    systray_button_click = 10;

    setup() {
        this.clicker = useClicker();
        this.action = useService("action");
    }

    openClickerGame() { 
        this.action.doAction({
            type: "ir.actions.client",
            tag: "awesome_clicker.client_action",
            target: "new",
            name:"Clicker"
        })
    }
}

export const systrayItem = {
    Component: ClickerSystray,
};

registry.category("systray").add("awesome_clicker.ClickerSystray", systrayItem, { sequence: 1000 });
