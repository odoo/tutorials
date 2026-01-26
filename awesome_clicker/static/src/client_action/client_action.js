import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useClicker } from "../utility";
import { ClickerValue } from "../clicker_value/clicker_value";

export class ClientAction extends Component {
    static template = "awesome_clicker.ClientAction";

    static components = {
        ClickerValue
    }

    setup() {
        this.clicker = useClicker();
    }

    bigIncrement() {
        this.clicker.increment(10_000);
    }

    buyClickBot() {
        this.clicker.buyClickBot();
    }

    buyBigClickBot() {
        this.clicker.buyBigClickBot();
    }

    buyPower() {
        this.clicker.buyPower();
    }
}

registry.category("actions").add("awesome_clicker.client_action", ClientAction)
