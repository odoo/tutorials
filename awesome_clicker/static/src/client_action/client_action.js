/** @odoo-module */

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

class ClickerClientAction extends Component {
    static template = "awesome_clicker.ClickerClientAction";
}

registry.category("actions").add("awesome_clicker.client_action", ClickerClientAction);
