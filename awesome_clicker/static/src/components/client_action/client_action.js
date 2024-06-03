/** @odoo-module **/
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useClicker } from "../../core/hooks";
import { ClickValue } from "../click_value/click_value";

export class ClientAction extends Component {
    static template = "awesome_clicker.client_action";
    static components = { ClickValue };

    setup() {
        this.clicker = useClicker();
    }

    onButtonClick() {
        this.clicker.increment(10);
    }
}

registry.category("actions").add("awesome_clicker.client_action", ClientAction);
