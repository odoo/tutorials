import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { useClicker } from "../utils";
import { ClickValue } from "../click_value";
import { doClickerAction } from "../clicker_service";

export class ClickerMenu extends Component {
    static template = "awesome_clicker.clicker_menu";
    static components = { ClickValue };

    setup() {
        this.clicker = useClicker();
        this.action = useService("action");
    }

    doAction() {
        doClickerAction(this.action);
    }
}

export const systrayItem = {
    Component: ClickerMenu,
};

registry.category("systray").add("awesome_clicker.clicker_menu", systrayItem);
