/** @odoo-module **/

import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static props = {
        size: {
            type: Number,
            optional: true
        }
    }

    static defaultProps = {
        size: 1
    }
    static template = "awesome_dashboard.dashboard_item";
}
