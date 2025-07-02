import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useClicker } from "../clicker_hook";
import { ClickerValue } from "../clicker_value/clicker_value";
import { useService } from "@web/core/utils/hooks";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";

class ClickerSystrayItem extends Component {
    static template = "clicker_systray_item.ClickerSystrayItem";
    static components = { ClickerValue, Dropdown, DropdownItem };

    setup() {
        super.setup();
        this.clicker = useClicker();
        this.action = useService("action");
    }

    openClickerClientAction() {
        this.action.doAction({
            type: "ir.actions.client",
            tag: "clicker_client_action.ClickerClientAction",
            name: "Clicker",
            target: "new",
        });
    }
}

registry.category("systray").add("clicker_systray_item.ClickerSystrayItem", {
    Component: ClickerSystrayItem
}, { sequence: 43 });
