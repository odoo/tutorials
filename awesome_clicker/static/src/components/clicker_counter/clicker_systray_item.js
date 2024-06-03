/** @odoo-module **/

import { Component, useExternalListener } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useClicker } from "../../core/hooks";
import { ClickValue } from "../click_value/click_value";

export class ClickerSystrayItem extends Component {
    static template = "awesome_clicker.clicker_systray_item";
    static components = { ClickValue };

    setup() {
        this.clicker = useClicker();

        useExternalListener(document.body, 'click', this.onClick, { capture: true });
    }

    onClick(event) {
        for (const button of document.querySelectorAll(".btn-clicker")) {
            if (button.contains(event.target)) return;
        }

        this.clicker.increment();
    }
}

const systrayItem = {
    Component: ClickerSystrayItem,
};

registry.category("systray").add("awesome_clicker.clicker_systray_item", systrayItem, { sequence: 1000 });
