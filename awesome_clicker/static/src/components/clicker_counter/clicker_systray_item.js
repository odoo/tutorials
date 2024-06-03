/** @odoo-module **/

import { Component, useExternalListener } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useClickerService } from "../../core/hooks";

export class ClickerSystrayItem extends Component {
    static template = "awesome_clicker.clicker_systray_item";

    setup() {
        this.clickerService = useClickerService();

        useExternalListener(document.body, 'click', this.onClick, { capture: true });
    }

    onClick(event) {
        for (const button of document.querySelectorAll(".btn-clicker")) {
            if (button.contains(event.target)) return;
        }

        this.clickerService.increment();
    }
}

const systrayItem = {
    Component: ClickerSystrayItem,
};

registry.category("systray").add("awesome_clicker.clicker_systray_item", systrayItem, { sequence: 1000 });
