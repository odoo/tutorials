import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { registry } from "@web/core/registry";
import { browser } from "@web/core/browser/browser";


export class DashboardSettingsDialog extends Component {
    static components = { Dialog };
    static template = "awesome_dashboard.SettingsDialog";

    setup() {
        const allItems = registry.category("awesome_dashboard").getAll();
        const removedIds = JSON.parse(browser.localStorage.getItem("awesome_dashboard.removed_ids") || "[]");
        
        this.items = useState(allItems.map(item => ({
            ...item,
            enabled: !removedIds.includes(item.id)
        })));
    }

    onApply() {
        const removedIds = this.items
            .filter(item => !item.enabled)
            .map(item => item.id);
        
        browser.localStorage.setItem("awesome_dashboard.removed_ids", JSON.stringify(removedIds));
        
        this.props.onConfigSaved();
        this.props.close();
    }
}