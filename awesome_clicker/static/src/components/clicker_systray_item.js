/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class ClickerSystrayItem extends Component {
    static template = "awesome_clicker.clicker_systray_item";

    setup() {
        this.state = useState({ counter: 0 });
    }

    increment() {
        this.state.counter++;
    }
}

const systrayItem = {
    Component: ClickerSystrayItem,
};

registry.category("systray").add("awesome_clicker.clicker_systray_item", systrayItem, { sequence: 1000 });
