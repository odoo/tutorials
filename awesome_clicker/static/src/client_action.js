/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useClicker } from "./clicker_hook";
import { ClickerValue } from "./clicker_value";

export class ClientAction extends Component {
    static template = "awesome_clicker.client_action";
    static props = {};
    static components = { ClickerValue };

    setup() {
        this.clickerHook = useClicker();
    }
}

registry.category("actions").add("awesome_clicker.client_action", ClientAction);
