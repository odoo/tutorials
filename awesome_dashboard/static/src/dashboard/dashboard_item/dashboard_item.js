import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem";
    static props = {
        title: String,
        size: Number,
        slots: Object
    };

    static defaultProps = {
        size: 1
    }
}
