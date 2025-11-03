import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useClicker } from "../clicker_hook";
import { ClickValue } from "../click_value/click_value";
import { Notebook } from "@web/core/notebook/notebook"

export class ClientAction extends Component {
    static template = "awesome_clicker.ClientAction";

    static components = { ClickValue, Notebook }

    static props = ["*"];

    setup() {
        this.clickerService = useClicker();
    }
    
}

registry.category("actions").add("awesome_clicker.ClientAction", ClientAction);
