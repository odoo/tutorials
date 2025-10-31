import { registry } from "@web/core/registry";
import { Component, useState, useExternalListener } from "@odoo/owl";

export class ClickerSystray extends Component {
    static template = "awesome_clicker.ClickerSystray";
    static props = {};

    setup() {
        this.state = useState({ counter: 0 });
        useExternalListener(window, "click", this.incrementBody, { capture: true });
    }

    increment() {
        this.state.counter+=9;
    }

    incrementBody() {
        this.state.counter++;
    }

}

export const systrayItem = {
    Component: ClickerSystray,
};

registry.category("systray").add("awesome_clicker.ClickerSystray", systrayItem, { sequence: 1000 });