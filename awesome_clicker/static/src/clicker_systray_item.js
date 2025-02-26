import { Component, useExternalListener, useState, xml } from "@odoo/owl";

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

class Clicker extends Component {
    static template = xml`<p>Clicks: <t t-esc="clicker.state.clicks"/></p><button class="o-dropdown dropdown-toggle dropdown" t-on-click.stop="onPlus"><i class="fa fa-plus"></i></button>
                        <button t-on-click="openAction" type="button" class="btn btn-primary">Open</button>`

    setup() {
        this.clicker = useState(useService("awesome_clicker.cliker_service"));
        this.action = useService("action");

        useExternalListener(window, "click", () => this.clicker.increment(1));
    }

    onPlus() {
        this.clicker.increment(10);
    }

    openAction() {
        this.action.doAction({
            type: 'ir.actions.client',
            name: 'Clicker',
            tag: 'awesome_clicker.client_action',
            target: 'new'
        });
    }
}

registry.category("systray").add("awesome_clicker.clicker", {
    Component: Clicker
});
