import { Component, useState } from "@odoo/owl";

import { registry } from "@web/core/registry";

import { useClicker } from "./clicker_service";
import { ClickValue } from "./click_value";

export class ClientAction extends Component {
    static template = "awesome_clicker.client_action";
    static components = { ClickValue };
    static props = {};

    setup() {
        this.clicker = useClicker();
    }
}

registry.category("actions").add("awesome_clicker.client_action", ClientAction);
