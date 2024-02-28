/** @odoo-module */

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";

import { Component } from "@odoo/owl";

import { useClicker } from "./use_clicker";
import { ClickValue } from "./click_value";

export class ClickerSystray extends Component {
    static template = "awesome_clicker.ClickerSystray";
    static components = { ClickValue, Dropdown, DropdownItem };
    static props = {};

    setup() {
        this.clicker = useClicker();
        this.action = useService("action");
    }

    openClientAction() {
        this.action.doAction({
            type: "ir.actions.client",
            tag: "awesome_clicker.client_action",
            target: "new",
            name: "Clicker"
        })
    }

    get numberTrees() {
        let sum = 0;
        for (const tree in this.clicker.trees) {
            sum += this.clicker.trees[tree].purchased;
        }
        return sum;
    }

    get numberFruits() {
        let sum = 0;
        for (const fruit in this.clicker.fruits) {
            sum += this.clicker.fruits[fruit];
        }
        return sum;
    }
}

registry.category("systray").add(
    "awesome_clicker.clicker_systray",
    {
        Component: ClickerSystray
    },
    {
        sequence: 100
    }
);

