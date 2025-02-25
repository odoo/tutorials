import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.dashboardItem";

    static props = {
        title: { type: String, optional: false },
    };
    static defaultProps = {
        size: 1
    }

}