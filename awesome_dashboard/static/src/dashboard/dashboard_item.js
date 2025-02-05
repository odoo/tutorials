/** @odoo-module **/

import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.dashboardItem";
    static props = {
        size: {type: Number, optional: true},
        slots: {type: Object}
    }
    static defaultProps= {
        size: 1
    }
}