import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.ConfigurationDialog";
    static components = { Dialog };

    static props = {
        items: Array,
        close: Function,
        onApply: Function,
    };

    setup() {
        this.state = useState({
            removedItems: JSON.parse(
                localStorage.getItem("awesome_dashboard_configuration") || "[]"
            ),
        });
    }

    isItemVisible(item) {
        return !this.state.removedItems.includes(item.id);
    }

    toggleItem = (itemId) => {
        if (this.state.removedItems.includes(itemId)) {
            this.state.removedItems =
                this.state.removedItems.filter((id) => id !== itemId);
        } else {
            this.state.removedItems.push(itemId);
        }
    };

    apply() {
        localStorage.setItem(
            "awesome_dashboard_configuration",
            JSON.stringify(this.state.removedItems)
        );

        this.props.onApply(this.state.removedItems);
        this.props.close();
    }
}