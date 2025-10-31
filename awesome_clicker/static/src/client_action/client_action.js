import {Component} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {useClicker} from "../useClicker";
import {ClickValue} from "../click_value/ClickValue";

export class ClientAction extends Component {
    static template = 'awesome_clicker.action'
    static props = {}
    static components = {ClickValue}

    setup() {
        this.clicker = useClicker();
    }

    canBuyClickBot() {
        return this.clicker.level > 0 && this.clicker.clicks >= 1000
    }

    canBuyBigBot() {
        return this.clicker.level > 1 && this.clicker.clicks >= 5000
    }

    canBuyPower() {
        return this.clicker.level > 2 && this.clicker.clicks >= 100000
    }
}

registry.category("actions").add("awesome_clicker.client_action", ClientAction);