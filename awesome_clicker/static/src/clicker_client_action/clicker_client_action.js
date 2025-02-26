import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useClicker } from "../clicker_hook";
import { ClickerValue } from "../clicker_value/clicker_value";

export class ClickerClientAction extends Component {
    static template = "clicker_client_action.ClickerClientAction";
    static components = { ClickerValue };

    setup() {
        super.setup();
        this.clicker = useClicker();
    }
}
registry.category("actions").add("clicker_client_action.ClickerClientAction", ClickerClientAction);
