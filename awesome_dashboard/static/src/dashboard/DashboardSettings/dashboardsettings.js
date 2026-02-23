import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Dialog } from "@web/core/dialog/dialog";

export class DashboardSettings extends Component {
    static template = "awesome_dashboard.settings";
    static components = { Dialog };
    static props = {
        title: { type: String, optional: true },
        removedItemIds: { type: Array, optional: true },
        applyConfiguration: { type: Function },
        close: { type: Function, optional: true },
    };

    setup() {
        this.items = registry.category("awesome_dashboard").getAll();
        const removedIds = new Set(this.props.removedItemIds || []);
        this.state = useState({
            enabledById: Object.fromEntries(this.items.map((item) => [item.id, !removedIds.has(item.id)])),
        });
    }

    isItemEnabled(item) {
        return this.state.enabledById[item.id] ?? true;
    }

    onToggleItem(ev) {
        const itemId = ev.currentTarget.dataset.itemId;
        this.state.enabledById[itemId] = ev.currentTarget.checked;
    }

    onApply() {
        const removedItemIds = this.items
            .filter((item) => !this.state.enabledById[item.id])
            .map((item) => item.id);
        this.props.applyConfiguration(removedItemIds);
        if (this.props.close) {
            this.props.close();
        }
    }
}
