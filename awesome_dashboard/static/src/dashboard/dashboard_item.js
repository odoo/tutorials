import { Component } from "@odoo/owl";

// Reusable dashboard item component with configurable size
export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem"
    static props = {
        slots: {
            type: Object,
            shape: {
                default: Object
            },
        },
        size: {
            type: Number,
            default: 1,
            optional: true,
        },
    };
}
