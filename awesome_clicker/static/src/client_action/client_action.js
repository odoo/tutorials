/** @odoo-module **/

import { Component } from "@odoo/owl";
import { Notebook } from "@web/core/notebook/notebook";
import { registry } from "@web/core/registry";
import { useClicker } from "../clicker_hook";
import { ClickerValue } from "../clicker_value/clicker_value";

export class ClientAction extends Component {
    static template = "awesome_clicker.ClientAction";
    static components = { ClickerValue, Notebook }

    setup() {
        this.clicker = useClicker();
    }
}

export const clientAction = {
    Component: ClientAction,
};

registry.category("actions").add("awesome_clicker.client_action", ClientAction);
