import { registry } from "@web/core/registry";
import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { useClicker } from "./clicker_hook";
import { ClickValue } from "./click_value/click_value";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";


class Clicker extends Component {
    static template = "awesome_clicker.clicker_systray_item";
    static components = { ClickValue, Dropdown, DropdownItem };

    setup(){
        this.clicker = useClicker();
        this.action = useService("action");
    }

    increment(){
        this.clicker.increment(9);
    }

    openClientAction(){
        this.action.doAction({
            type: "ir.actions.client",
            tag: "awesome_clicker.client_action",
            target: "new",
            name: "Clicker Game"
        });
    }

    get numberTrees() {
        let sum = 0;
        for(const tree in this.clicker.trees){
            sum += this.clicker.trees[tree].purchased;
        }
        return sum;
    }

    get numberFruits() {
        let sum = 0;
        for(const fruit in this.clicker.fruits){
            sum += this.clicker.fruits[fruit];
        }
        return sum;
    }

    get numberBots(){
        let sum = 0;
        for(const bot in this.clicker.bots){
            sum += this.clicker.bots[bot].purchased;
        }
        return sum;
    }

}

registry.category("systray").add("awesome_clicker.Clicker", { Component: Clicker });
