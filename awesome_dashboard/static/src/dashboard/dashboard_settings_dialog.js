import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class DashboardSettingsDialog extends Component {
    static template = "awesome_dashboard.SettingsDialog";
    static components = { Dialog };

    setup() {
        this.state = useState({
            selected: new Set(
                this.props.items
                    .map((item) => item.id)
                    .filter((id) => !this.props.removedItems.includes(id))
            ),
        });
    }

    toggleItem(id) {
    const newSet = new Set(this.state.selected);

        if (newSet.has(id)) {
            newSet.delete(id);
        } else {
            newSet.add(id);
        }

    this.state.selected = newSet;
    }

    apply() {
        const removed = this.props.items
            .map((item) => item.id)
            .filter((id) => !this.state.selected.has(id));

        this.props.onApply(removed);
            if (this.props.close) {
            this.props.close();
        }
    }
}