import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useClicker } from "../utils";

export class ClickerAction extends Component {
    static template = "awesome_clicker.clicker_action";

    setup() {
        this.clicker = useClicker();
    }
}

registry.category("actions").add("awesome_clicker.clicker_action", ClickerAction);
