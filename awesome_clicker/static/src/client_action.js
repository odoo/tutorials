/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useClicker } from "./clicker_hook";
import { ClickValue } from "./click_value";

export class ClientAction extends Component {
    static template = "awesome_clicker.client_action";

    static components = { ClickValue }

    setup() {
        this.clicker = useClicker()
    }

}


registry.category("actions").add("awesome_clicker.client_action", ClientAction)
