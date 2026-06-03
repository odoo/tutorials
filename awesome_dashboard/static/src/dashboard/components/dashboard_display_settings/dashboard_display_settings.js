import { Component } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class DashboardSettingsDialog extends Component {
    static template = "awesome_dashboard.DashboardSettingsDialog";
    static components = {
        Dialog,
    };

    setup() {
        this.removedIds = new Set(
            JSON.parse(
                localStorage.getItem("dashboard_config") || "[]"
            )
        );
    }

    isChecked(id) {
        return !this.removedIds.has(id);
    }

    toggleItem(id, ev) {
        if (ev.target.checked) {
            this.removedIds.delete(id);
        } else {
            this.removedIds.add(id);
        }
    }

    apply() {
        localStorage.setItem(
            "dashboard_config",
            JSON.stringify([...this.removedIds])
        );

        this.props.close();
    }
}