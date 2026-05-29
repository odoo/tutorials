/** @odoo-module **/
import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { registry } from "@web/core/registry";

export class DashboardConfigDialog extends Component {
    static components = { Dialog };
    static template = "awesome_dashboard.DashboardConfigDialog";

    setup() {
        this.allItems = registry.category("awesome_dashboard").getAll();
        
        const disabledItems = JSON.parse(localStorage.getItem("disabled_dashboard_items") || "[]");
        
        const initialStatus = {};
        for (const item of this.allItems) {
            initialStatus[item.id] = !disabledItems.includes(item.id);
        }
        
        this.state = useState(initialStatus);
    }

    onApply() {
        const disabledIds = Object.keys(this.state).filter(id => !this.state[id]);
        
        localStorage.setItem("disabled_dashboard_items", JSON.stringify(disabledIds));
        
        this.props.onConfigSaved();
        
        this.props.close();
    }
}
