import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.dashboard-item";
    static props = {
        size: Number,
        slots: { type: Object, optional: true },
    };
}
