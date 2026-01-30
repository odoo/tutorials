import { Component } from "@odoo/owl";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

import { useClicker } from "../clicker_service";
import { ClickValue } from "../click_value/click_value";


export class ClickerSystrayItem extends Component {
    static template = "awesome_clicker.ClickerSystrayItem";
    static components = { ClickValue, Dropdown, DropdownItem };

    setup() {
        this.clicker = useClicker();
        this.action_service = useService("action");
    }

    openClickerWindow() {
        this.action_service.doAction({
            type: "ir.actions.client",
            tag: "awesome_clicker.client_action",
            target: "new",
            name: "Clicker"
        });
    }
}

registry.category("systray").add("awesome_clicker.ClickerSystrayItem", { Component: ClickerSystrayItem });
