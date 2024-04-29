/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

class ClientAction extends Component {
    static template = "awesome_clicker.ClientAction"
}

registry.category("actions").add("awesome_clicker.client_action", ClientAction);