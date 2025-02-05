/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";
import { dashboardRegistry } from "../dashboard_items/dashboard_items";

export class SettingsDialog extends Component {
    static template = "awesome_dashboard.SettingsDialog";
    static components = { Dialog };

    setup() {
        this.dialog = useService("dialog");
        this.items = Object.values(dashboardRegistry.getAll());
        this.state = useState({
            hidden_dashboard_items: new Set(this.props.hidden_dashboard_items),
        });
    }

    toggleItem(event) {
        const id = event.target.id;
        this.state.hidden_dashboard_items.has(id) ? this.state.hidden_dashboard_items.delete(id) : this.state.hidden_dashboard_items.add(id);
    }

    applySettings() {
        this.props.onApply([...this.state.hidden_dashboard_items]);
        this.dialog.closeAll();
    }
}