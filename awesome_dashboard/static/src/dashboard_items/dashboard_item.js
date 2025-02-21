import { Component } from "@odoo/owl";

export class DashboardItems extends Component {
    static template = "awesome_dashboard.item"

    static props = {
        title: { type: String },
        slot: { type: Object, optional: true },
        size: { type: Number, optional: true }
    }

    static defaultProps = {
        size: 1
    }

}