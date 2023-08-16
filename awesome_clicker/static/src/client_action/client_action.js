import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

class ClickerClientAction extends Component {
    static template = "awesome_clicker.ClickerClientAction";
    static props = ["*"];
}

registry.category("actions").add("awesome_clicker.client_action", ClickerClientAction);
