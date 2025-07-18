import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem";
    static props = {
        size: {
            type: Number,
            optional: true,
            default: 1,
        },
        slots: {
            type: Object,
            optional: true,
        }
    }

    get cardStyle() {
        return `width: ${this.props.size * 18}rem;`;
    }
}