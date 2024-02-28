/** @odoo-module */

import { registry } from "@web/core/registry";
import { Notebook } from "@web/core/notebook/notebook";

import { Component } from "@odoo/owl";

import { useClicker } from "./use_clicker";
import { ClickValue } from "./click_value";

export class ClientAction extends Component {
    static template = "awesome_clicker.ClientAction";
    static components = { ClickValue, Notebook };
    setup() {
        this.clicker = useClicker();
    }
}

registry.category("actions").add("awesome_clicker.client_action", ClientAction);
