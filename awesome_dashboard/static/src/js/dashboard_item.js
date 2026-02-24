import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem";

    // Default value
    static defaultProps = {
        size: 1,  // if parent doesn't provide `size`, it will be 1
    };

    static props = {
        size: { type: Number, optional: true },
    };

    get width() {
        return `width: ${18 * this.props.size}rem`;
    }
}