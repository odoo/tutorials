import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { registry } from "@web/core/registry";
import { browser } from "@web/core/browser/browser";

export class ConfigurationDialog extends Component {
    static components = { Dialog };
    static template = "awesome_dashboard.ConfigurationDialog";

    setup() {
        const allItems = registry.category("awesome_dashboard").getAll();
        this.state = useState({
            items: allItems.map((item) => ({
                ...item,
                isEnabled: !this.props.initialRemovedItems.includes(item.id),
            })),
        });
    }

    apply() {
        const removedIds = this.state.items
            .filter((i) => !i.isEnabled)
            .map((i) => i.id);
        
        browser.localStorage.setItem("dashboard_removed_items", JSON.stringify(removedIds));
        
        this.props.onApply(removedIds);
        this.props.close();
    }
}