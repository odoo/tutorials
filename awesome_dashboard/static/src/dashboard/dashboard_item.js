/** @odoo-module **/

import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.dashboardItem";
    static props = {
        size: {type: Number}
    }
    static defaultProps= {
        size: 1
    }
}