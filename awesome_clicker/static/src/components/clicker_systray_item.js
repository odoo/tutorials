/** @odoo-module **/

import { Component, useExternalListener, useRef, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class ClickerSystrayItem extends Component {
    static template = "awesome_clicker.clicker_systray_item";

    setup() {
        this.state = useState({ counter: 0 });
        this.counterButtonRef = useRef('awesome_clicker.counter_button');

        useExternalListener(document.body, 'click', this.onClick, { capture: true });
    }

    onClick(event) {
        if (this.counterButtonRef.el.contains(event.target)) return;

        this.state.counter++;
    }

    onButtonClick() {
        this.state.counter += 10;
    }
}

const systrayItem = {
    Component: ClickerSystrayItem,
};

registry.category("systray").add("awesome_clicker.clicker_systray_item", systrayItem, { sequence: 1000 });
