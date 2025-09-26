import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.dashboard_item";
    static props = {
        size: {
            type: Number,
            defaultProps: 1,
            optional: true,
        },
        slots: {
            type: Object,
        },
    };
    get Width() {
        return 18*this.props.size
    }
}

