/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { useClicker } from "./clicker_hook";
import { ClickerValue } from "./clicker_value";

class ClientAction extends Component {
    static template = "awesome_clicker.ClientAction";
    static components = { ClickerValue };

    setup() {
        this.clicker_hook = useClicker();
    }
}

registry.category("actions").add("awesome_clicker.client_action", ClientAction);
