import { Component } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { registry } from "@web/core/registry";

export class DashboardConfigDialog extends Component {
    static template = "awesome_dashboard.DashboardConfigDialog";
    static components = { Dialog };
    static props = {
        close: Function,
        onApply: Function,
        currentConfig: Array,
    };

    setup() {
        this.allItems = registry.category("awesome_dashboard").getAll();
        this.hiddenItems = new Set(this.props.currentConfig);
    }

    toggleItem = (itemId) => {
        if (this.hiddenItems.has(itemId)) {
            this.hiddenItems.delete(itemId);
        } else {
            this.hiddenItems.add(itemId);
        }
    }

    isItemVisible = (itemId) => {
        return !this.hiddenItems.has(itemId);
    }

    apply = () => {
        this.props.onApply(Array.from(this.hiddenItems));
        this.props.close();
    }
}
