import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { useClicker } from "./clicker_hook";
import { ClickValue } from "./clicker_value";



class ClientAction extends Component {
    static template = "awesome_clicker.ClientAction";
    static components = { ClickValue: ClickValue };
    setup() {
        this.clicker = useClicker();
    }

    increment(event) {
        this.clicker.increment(9);
    }
}

registry.category("actions").add("awesome_clicker.client_action", ClientAction);
