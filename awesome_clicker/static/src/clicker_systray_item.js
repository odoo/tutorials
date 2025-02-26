import { Component, useExternalListener, useState, xml } from "@odoo/owl";

import { registry } from "@web/core/registry";

class Clicker extends Component {
    static template = xml`<p>Clicks: <t t-esc="state.count"/></p><button class="o-dropdown dropdown-toggle dropdown" t-on-click.stop="onPlus"><i class="fa fa-plus"></i></button>`

    setup() {
        this.state = useState({ count: 0 });

        useExternalListener(window, "click", () => this.state.count++);
    }

    onPlus() {
        this.state.count += 10;
    }
}

registry.category("systray").add("awesome_clicker.clicker", {
    Component: Clicker
});
