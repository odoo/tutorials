import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem";

    static props = {
        size: { type: Number, optional: true },
    };

    get width() {
        const size = this.props.size || 1;
        return `${18 * size}rem`;
    }
}
