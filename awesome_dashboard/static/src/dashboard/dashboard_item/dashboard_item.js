import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.dashboard_item";
    static props = {
        size: { optional: true},
        slots: { optional: true }
    };
    static defaultProps = {
        size: 1
    };
}