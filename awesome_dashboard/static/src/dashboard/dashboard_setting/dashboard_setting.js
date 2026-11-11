import {Component, useState} from "@odoo/owl";
import {Dialog} from "@web/core/dialog/dialog";

export class DashboardSettings extends Component {
    static template = "awesome_dashboard.DashboardSettings";
    static components = {Dialog};

    static props = {
        items: Array,
        removedItems: Array,
        close: Function,
        onApply: Function,
    };

    setup() {
        this.state = useState({
            removedItems: [...this.props.removedItems],
        });
    }

    toggleItem(itemId, checked) {
        if (checked) {
            this.state.removedItems = this.state.removedItems.filter(
                (id) => id !== itemId
            );
        } else if (!this.state.removedItems.includes(itemId)) {
            this.state.removedItems.push(itemId);
        }
    }

    apply() {
        this.props.onApply(this.state.removedItems);
        this.props.close();
    }
}