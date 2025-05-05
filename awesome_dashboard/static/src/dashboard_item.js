import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem";
    static props = {
        slots: {
            type: Object,
            optional: true,
        },
        size: {
            type: Number,
            optional: true,
            // default: 1, // doesn't work
        },
    };

    setup() {
        // Default size value
        if (!this.props.size) {
            this.props.size = 1;
        }
    }
}
