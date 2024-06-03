/** @odoo-module **/
import { Component, useExternalListener } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { useClicker } from "./clicker_service";
import { ClickerValue } from "./clicker_value";

export class ClickerSystrayItem extends Component {
    setup() {
        this.action = useService("action");
        this.clicker = useClicker();

        useExternalListener(document.body, "click", this.globalOnClick, { capture: true });
    }

    globalOnClick(event) {
        if (!(event.target.id === "increment_click_button")) {
            this.clicker.increment(1);
        }

    }

    onOpenClick() {
        this.action.doAction({
            type: "ir.actions.client",
            tag: "awesome_clicker.client_action",
            target: "new",
            name: "Clicker",
        });
    }
}

ClickerSystrayItem.template = "awesome_clicker.clicker_systray_item";
ClickerSystrayItem.components = { ClickerValue };

registry.category("systray").add("awesome_clicker.clicker_systray_item", { Component: ClickerSystrayItem });