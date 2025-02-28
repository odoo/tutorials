/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Notebook } from "@web/core/notebook/notebook";
import { useClicker } from "./clicker_service";
import { ClickValue } from "./click_value";

export class ClickerClientAction extends Component {
    static template = "awesome_clicker.ClickerClientAction";

    static components = { ClickValue, Notebook };

    setup() {
        this.clicker = useClicker();
    }
}

registry.category("actions").add("awesome_clicker.ClickerClientAction", ClickerClientAction);
