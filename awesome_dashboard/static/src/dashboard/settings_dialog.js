import { Component, useState, useEnv } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class DashboardSettingsDialog extends Component {
    static template = "awesome_dashboard.DashboardSettingsDialog";
    static components = { Dialog };
    static props = {
        items: Array,
        removedItems: Array,
        onApply: Function,
        close: Function,
    };

    setup() {
        this.env = useEnv();
        this.state = useState({
            unchecked: new Set(this.props.removedItems),
        });
    }

    toggleItem(id) {
        if (this.state.unchecked.has(id)) {
            this.state.unchecked.delete(id);
        } else {
            this.state.unchecked.add(id);
        }
    }

    apply() {
        this.props.onApply([...this.state.unchecked]);
        this.props.close();
    }
}
