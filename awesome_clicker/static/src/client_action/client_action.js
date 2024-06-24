/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

export class ClientAction extends Component {
    static template = "awesome_clicker.ActionButton";
}

registry.category("actions").add("awesome_clicker.client_action", ClientAction);