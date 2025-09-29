import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class DashboardItemsDialog extends Component {
    static template = 'awesome_dashboard.DashboardItemsDialog';
    static components = { Dialog };
    static props = {
        items: {
            type: Array,
            element: {
                type: Object,
                shape: {
                    id: String,
                    description: String,
                    "*": true,
                },
            },
        },
        excludedItems: {
            type: Array,
            element: String,
        },
        close: Function,
        onApply: Function,
    };

    setup() {
        this.state = useState({
            items: this.props.items.map(
                item => ({
                    ...item,
                    checked: !this.props.excludedItems.includes(item.id),
                }),
            ),
        });
    }

    toggle(event) {
        const index = this.state.items.findIndex(item => item.id === event.target.name);
        if (index !== -1) {
            this.state.items[index].checked = !this.state.items[index].checked;
        }
    }

    apply() {
        const newExcludedItems = this.state.items.filter(item => !item.checked).map(item => item.id);
        this.props.onApply(newExcludedItems);
        this.props.close();
    }
}
