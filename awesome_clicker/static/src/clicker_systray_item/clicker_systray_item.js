import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useClicker } from "../clicker_hook";
import { useService } from "@web/core/utils/hooks";
import { ClickValue } from "../click_value/click_value";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";

export class ClickerSystrayItem extends Component {
    static template = "awesome_clicker.ClickerSystrayItem";

    static components = { ClickValue, Dropdown, DropdownItem }

    static props = {}

    setup() {
        this.clickerService = useClicker();
        this.action = useService("action");
    }

    openClientAction() {
        this.action.doAction(
            {
                type: "ir.actions.client",
                tag: "awesome_clicker.ClientAction",
                target: "new",
                name: "Clicker Game"
            }
        )
    }

    get totalFruits() {
        let totalFruits = 0;
        for(const fruit in this.clickerService.fruits) {
            totalFruits += this.clickerService.fruits[fruit];
        }
        return totalFruits;
    }

    get totalTrees() {
        let totalTrees = 0;
        for(const tree in this.clickerService.trees) {
            totalTrees += this.clickerService.trees[tree].number;
        }
        return totalTrees;
    }
    
}

export const systrayItem = {
    Component: ClickerSystrayItem,
};

registry.category("systray").add("awesome_clicker.ClickerSystrayItem", systrayItem);
