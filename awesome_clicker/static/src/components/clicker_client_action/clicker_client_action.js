import { Component, useState, useExternalListener } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useClicker } from "../clicker_hook";
import { ClickValue } from "../click_value";
import { ClickBot } from "../click_bot";
import { PowerBuy } from "../power_buy";
import { Tree } from "../tree";
import { Fruits } from "../fuit";
import { Notebook } from "@web/core/notebook/notebook";

export class ClickerClientAction extends Component {
    static props = {};
    static template = "clicker_client_action.ClickerClientAction";
    static components = { ClickValue, ClickBot, PowerBuy, Tree, Fruits, Notebook };
    setup() {
        this.state = useClicker();
    }

    increment_button(event) {
        event.stopPropagation();
        this.state.increment(10000);
    }
}

registry.category("actions").add("awesome_clicker.client_action", ClickerClientAction);