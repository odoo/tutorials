import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { registry } from "@web/core/registry";

export class ConfigDialog extends Component {
    static template = "awesome_dashboard.ConfigDialog";
    static components = { Dialog };

    setup() {
        this.items = registry.category("awesome_dashboard").get("DashboardItems");
        this.state = useState({
            hiddenIds: this.props.hiddenIds,
        });
    }

    toggleItem(id) {
        console.log(this.state.hiddenIds);
        const idIndex = this.state.hiddenIds.indexOf(id);
        if (idIndex >= 0) {
            this.state.hiddenIds.splice(idIndex, 1);
        } else {
            this.state.hiddenIds.push(id);
        }
    }

    onApply() {
        this.props.onApply(this.state.hiddenIds);
        this.props.close();
    }
}
