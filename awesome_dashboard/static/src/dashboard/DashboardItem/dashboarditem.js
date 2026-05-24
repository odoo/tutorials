import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "dashboardItemjj"
    static components = {}

    static props = {
        size: {type: Number},
        slots: {type: Object}
    }

    static defaultProps = {
        size: 1,
        slots: true
    }
}
