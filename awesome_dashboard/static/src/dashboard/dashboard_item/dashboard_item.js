import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.item";
    static props = {
        size: { type: Number, optional: true },
    };
    static defaultProps = {
        size : 1
    }
}
