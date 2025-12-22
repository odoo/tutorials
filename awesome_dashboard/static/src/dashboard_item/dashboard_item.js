import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem";
    static props = {
        size: {
            type: Number,
            default: 1,
        },
        slots: {
            type: Object,
            shape: {
                default: true,
            },
        },
    };

    setup() {
        console.log("This item has a size of " + this.props.size);
    }
}
