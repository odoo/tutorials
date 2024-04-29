/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { ClickerValue } from "./clicker_value";
import { useClicker } from "./clicker_hook";

class ClientAction extends Component {
    static template = "awesome_clicker.ClientAction";
    static components = { ClickerValue };

    setup() {
        this.clicker_hook = useClicker();
    }

    buyClickBot() {
        this.clicker_hook.clicks -= 1000;
        this.clicker_hook.clickBots += 1;
    }

    buyBigBot() {
        this.clicker_hook.clicks -= 5000;
        this.clicker_hook.bigBots += 1;
    }

    buyPower(){
        this.clicker_hook.clicks -= 50000;
        this.clicker_hook.power += 1;
    }
}

registry.category("actions").add("awesome_clicker.client_action", ClientAction);
