import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem";

    static props = {
        size: { type: Number, optional: true },
    };

    get width() {
        return 18 * (this.props.size || 1);
    }
}
