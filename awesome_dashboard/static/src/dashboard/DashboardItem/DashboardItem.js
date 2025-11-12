import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem";

    static props = {
        title: String,
        size: { optional: true },
        slots: { type: Object, optional: true},
    };

    static defaultProps = {
        size: 1,
    }

}
