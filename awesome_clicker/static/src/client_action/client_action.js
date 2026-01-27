import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useClicker } from "../utility";
import { ClickerValue } from "../clicker_value/clicker_value";
import { treeTypes } from "../models/clicker_model";
import { Notebook } from "@web/core/notebook/notebook";


export class ClientAction extends Component {
    static template = "awesome_clicker.ClientAction";

    static components = {
        ClickerValue,
        Notebook
    }

    setup() {
        this.clicker = useClicker();
    }

    bigIncrement() {
        this.clicker.increment(100_000);
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

    buyTree(fruitName) {
        this.clicker.buyTree(fruitName);
    }

    getTreeTypes() {
        return treeTypes;
    }
}

registry.category("actions").add("awesome_clicker.client_action", ClientAction)
