/** @odoo-module **/
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class ClickerSystrayOpenButton extends Component {
    static template = "awesome_clicker.clicker_systray_open_button";

    setup() {
        this.actionService = useService("action");
    }

    openClientAction() {
        this.actionService.doAction({
            type: "ir.actions.client",
            tag: "awesome_clicker.client_action",
            target: "new",
            name: "Clicker",
        });
    }
}

const systrayItem = {
    Component: ClickerSystrayOpenButton,
};
registry.category("systray").add("awesome_clicker.clicker_systray_open_button", systrayItem, { sequence: 999 });
