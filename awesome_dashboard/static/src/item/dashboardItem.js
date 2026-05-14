import { Component } from "@odoo/owl"

export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem";

    static props = {
        size: Number,
        slots: { optional: true }
    }

    static defaultSize = {
        size: 1
    }
}
