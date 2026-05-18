import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "dashboardItem"
    static components = {}

    static props = ["size?","slots?"]

    static defaultProps = {
        size: 1,
        slots: true
    }
}
