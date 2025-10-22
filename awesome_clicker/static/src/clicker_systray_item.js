import { Component, useExternalListener } from '@odoo/owl'
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { useClicker } from "./hooks";
import { ClickValue } from './ClickValue';
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";

export class ClickerSystray extends Component {
    static template = "awesome_clicker.ClickerSystray";
    static components = { ClickValue, Dropdown, DropdownItem }

    setup() {
        this.clicker = useClicker();
        this.action = useService("action");
        useExternalListener(document.body, "click", () => this.clicker.increment(1), { capture: true });
    }

    openClicker = () => {
        this.action.doAction({
            type: "ir.actions.client",
            tag: "awesome_clicker.client_action",
            target: "new",
            name: "Clicker Game",
        });
    }
}

export const systrayItem = {
    Component: ClickerSystray,
};

registry.category("systray").add("awesome_clicker.ClickerSystray", systrayItem, { sequence: 10 });
