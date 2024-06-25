/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { Notebook } from "@web/core/notebook/notebook";

import { useClicker } from "../clicker_hook.js"
import { ClickerValue } from "../clicker_value/clicker_value.js";


export class ClientAction extends Component {
    static template = "awesome_clicker.ActionButton";
    static props = {
        description: { type: String, optional: true },
        action: Object,
        actionId: { type: Number, optional: true }
    };
    static components = { ClickerValue, Notebook };

    setup() {
        this.clicker = useClicker();
    }

    incrementButtonAction() {
        this.clicker.increment(9);
    }
}

registry.category("actions").add("awesome_clicker.client_action", ClientAction);