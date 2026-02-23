import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.dashboardItem";
    static props = {
        size: { type: Number, default: 1, optional: true }
    };

    get cardStyle() {
        const width = 18 * this.props.size;
        return `width: ${width}rem;`;
    }
}
