import { Component } from "@odoo/owl"

export class DashboardItem extends Component {
    static template = "awesome_dashboard.dashboarditem";
    static props = {
        size: {
            type: Number,
            default: 1,
            optional: true,
        },
        slots: Object,
    };
}
