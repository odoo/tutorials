import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { ClickerValue } from "../clicker_value/clicker_value";
import { ClickBots } from "../click_bots/click_bots";
import { Notebook } from "@web/core/notebook/notebook";
import { useClicker } from "../clicker_hook";

export class ClickerClientAction extends Component {
    static template = "clicker_client_action.ClickerClientAction";
    static components = { ClickerValue, ClickBots, Notebook };

    setup() {
        super.setup();
        this.clicker = useClicker();
    }
}
registry.category("actions").add("clicker_client_action.ClickerClientAction", ClickerClientAction);
