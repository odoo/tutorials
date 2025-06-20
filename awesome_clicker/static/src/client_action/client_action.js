import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useClicker } from "../clickerService";
import { ClickerValue } from "../clicker_value/clicker_value";

export class ClickerClientAction extends Component {
    static template = "awesome_clicker.ClickerClientAction"
    
    static components = { ClickerValue }
    
    static props = ["*"]

    setup(){
        this.clicker = useClicker();
    }
}

registry.category("actions").add("awesome_clicker.client_action", ClickerClientAction);