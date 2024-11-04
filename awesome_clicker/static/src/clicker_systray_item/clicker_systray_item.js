/** @odoo-module **/

import {registry} from "@web/core/registry";
import {Component} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";
import {useClicker} from "../clicker_hook";
import {ClickerValue} from "../click_value/click_value";
import {Dropdown} from "@web/core/dropdown/dropdown";
import {DropdownItem} from "@web/core/dropdown/dropdown_item";


class ClickerSystrayItem extends Component {
    static template = "awesome_clicker.ClickerSystrayItem";
    static props = {};
    static components = {ClickerValue, Dropdown, DropdownItem};

    setup() {
        this.clicker = useClicker();
        this.action = useService("action");
    }


    openClientAction() {
        this.action.doAction({
            type: "ir.actions.client",
            tag: "awesome_clicker.client_action",
            target: "new",
            name: "Clicker Menu",
        });
    }

}

const item = {
    Component: ClickerSystrayItem
};

registry.category("systray").add("awesome_clicker.ClickerSystrayItem", item, {sequence: 43});
