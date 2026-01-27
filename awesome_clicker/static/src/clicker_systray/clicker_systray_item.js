import { Component, useExternalListener } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { useClicker } from "../utility";
import { ClickerValue } from "../clicker_value/clicker_value";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";
import { Dropdown } from "@web/core/dropdown/dropdown"
import { treeTypes } from "../models/clicker_model";

export class ClickerSystrayItem extends Component {
    static template = "awesome_clicker.ClickerSystrayItem";

    static components = {
        ClickerValue,
        Dropdown,
        DropdownItem
    }

    setup() {
        this.clicker = useClicker();
        this.actionService = useService("action");

        useExternalListener(document, "click", this.increment, {capture: true})
    }

    bigIncrement() {
        this.clicker.increment(10);
    }

    increment(ev) {
        if(ev.target.closest("#clicker-big-increment-button")) return;

        this.clicker.increment(1);
    }

    openClientAction() {
        this.actionService.doAction({
            type: 'ir.actions.client',
            tag: 'awesome_clicker.client_action',
            target: 'new',
            name: 'Clicker'
        })
    }

    getTreeTypes() {
        return treeTypes;
    }
}

registry.category("systray").add("awesome_clicker.client_action", {
    Component: ClickerSystrayItem,
    sequence: 1
});
