import { Component, onWillStart, useState, useExternalListener} from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { useClicker } from "../clicker_hook/clicker_hook";
import { ClickValue } from "../click_value/click_value";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";

class ClickerSystrayItem extends Component {
    static template = "awesome_clicker.clicker_systray_item";
    static components = {ClickValue, Dropdown, DropdownItem  };
    static props =[];
    
    setup()
    {
        this.action = useService("action");
        this.clicker = useClicker();
    }
    onOpen()
    {
        this.action.doAction({
            type: "ir.actions.client",
            tag: "awesome_clicker.client_action",
            target: "new",
            name: "Clicker"
        })
    }
    get allTrees()
    {
        let sum = 0;
        for(const tree in this.clicker.trees)
            {
                sum += this.clicker.trees[tree].quantity;
            }
        return sum;
    }
    get allFruits()
    {
        let sum = 0;
        for(const tree in this.clicker.trees)
            {
                sum += this.clicker.trees[tree].fruit;
            }
        return sum;
    }


}
export const sysItem = {
    Component: ClickerSystrayItem
}
registry.category("systray").add("awesome_clicker.clickerSystrayItem",sysItem, {sequence:10000})
