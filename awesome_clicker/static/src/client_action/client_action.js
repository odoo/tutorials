/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useClicker } from "../use_clicker";
import { ClickValue } from "../click_value/click_value";

class ClientAction extends Component {
    static template = "awesome_clicker.ClientAction";
    static components = { ClickValue };

    setup() {
        this.clicker = useClicker();
    }

    onButtonClick() {
        const CLICK_BONUS = 999;
        this.clicker.increment(CLICK_BONUS);
    }

    buyClickBot() {
        this.clicker.buyBot("clickbot");
    }

    buyBigBot() {
        this.clicker.buyBot("bigbot");
    }

    purchasePowerLevel(){
        this.clicker.purchasePowerLevel();
    }

}

registry.category("actions").add("awesome_clicker.client_action", ClientAction);