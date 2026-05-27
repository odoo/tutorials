import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem";
    
    static props = {
        size: { type: Number, optional: true },
        slots: { type: Object, optional: true },
    };

    get size() {
        return this.props.size || 1;
    }
}