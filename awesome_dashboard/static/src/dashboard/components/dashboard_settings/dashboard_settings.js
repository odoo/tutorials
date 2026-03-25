
import { Component, useState } from "@odoo/owl";

export class DashboardSettings extends Component {
    static template = "awesome_dashboard.DashboardSettings";
    static props = {
        items: Array,
        onApply: Function,
    };
    setup() {
        this.state = useState({
            selected: {},
        });
        for (const item of this.props.items) {
            this.state.selected[item.id] = true;
        }
    }
    toggleItem(id) {
        this.state.selected[id] = !this.state.selected[id];
    }
    apply() {
        const removed = [];

        for (const [id, isSelected] of Object.entries(this.state.selected)) {
            if (!isSelected) {
                removed.push(id);
            }
        }
        this.props.onApply(removed);
    }
}
