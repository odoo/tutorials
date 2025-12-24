import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class ClickerAction extends Component {
    static template = "awesome_clicker.clicker_action";
}

registry.category("actions").add("awesome_clicker.clicker_action", ClickerAction);
