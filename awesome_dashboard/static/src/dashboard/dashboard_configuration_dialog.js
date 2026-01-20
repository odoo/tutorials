/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class DashboardConfigurationDialog extends Component {
    static template = "awesome_dashboard.DashboardConfigurationDialog";

    static components = { Dialog };

    static props = ["disabled", "available", "apply", "close"];

    setup() {
        this.items = useState(this.props.available.map((item) => {
            return {
                id: item.id,
                description: item.description,
                enabled: !this.props.disabled.has(item.id),
            };
        }));
        this.toggleItem = this.toggleItem.bind(this);
    }

    apply() {
        this.props.apply(new Set(this.items
            .filter((item) => !item.enabled)
            .map((item) => item.id)
        ));
        this.props.close();
    }

    toggleItem(id) {
        const item = this.items.find((i) => i.id == id);
        item.enabled = !item.enabled;
    }
}
