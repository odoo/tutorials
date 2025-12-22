import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.dashboard-item";
    static props = {
        size: { type: Number, optional: true },
        title: String,
        slots: { type: Object, optional: true },
    };
    static defaultProps = {
        size: 1,
    };
}
