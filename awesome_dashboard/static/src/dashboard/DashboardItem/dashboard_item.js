import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem";
    static props = {
        title: {
            type: String,
            optional: true
        },
        slots: {
            type: Object,
            shape: {
                default: Object,
            },
        },
        size: {
            type: Number,
            optional: true,
        },
    };
}
