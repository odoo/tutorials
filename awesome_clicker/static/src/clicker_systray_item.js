/** @odoo-module **/

import { Component } from "@odoo/owl";
import { humanNumber } from "@web/core/utils/numbers";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";
import { ClickValue } from "./click_value";
import { useClicker } from "./clicker_service";

export class ClickerSystrayItem extends Component {
    static template = "awesome_clicker.ClickerSystrayItem";

    static components = { ClickValue, Dropdown, DropdownItem };

    setup() {
        this.action = useService("action");
        this.clicker = useClicker();
    }

   openClientAction() {
        this.action.doAction({
            type: "ir.actions.client",
            tag: "awesome_clicker.ClickerClientAction",
            target: "new",
            name: "Clicker Game",
        });
    }

    formattedClicks() {
        return humanNumber(this.clicker.clicks);
    }
}

export const systrayItem = {
    Component: ClickerSystrayItem,
}

registry.category("systray").add("awesome_clicker.ClickerSystrayItem", systrayItem, { sequence: 1000 });
