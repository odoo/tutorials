/** @odoo-module **/

import { registry } from "@web/core/registry";

import { Component, useState } from "@odoo/owl";
import { useClicker } from "./clicker_service";
import { ClickerValue } from "./clicker_value";

class ClientAction extends Component {
    setup() {
        this.clicker = useClicker();
    }

    onIncrement() {
        this.clicker.increment(1000);
    }

    onBuyClickBot() {
        this.clicker.buyClickBot();
    }

    onBuyBigClickBot() {
        this.clicker.buyBigClickBot();
    }

    onBuyPower() {
        this.clicker.buyPower();
    }
}

ClientAction.template = "awesome_clicker.client_action";
ClientAction.components = { ClickerValue };

registry.category("actions").add("awesome_clicker.client_action", ClientAction);