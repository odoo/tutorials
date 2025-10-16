import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem"
    static props = { 
        size: {type: Number, optional: true},
        slots: {optional: true}
    };

    setup() {
        this.size = this.props.size || 1;
    }
}
