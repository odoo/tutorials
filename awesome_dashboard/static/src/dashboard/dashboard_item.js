/** @odoo-module **/

import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.dashboard_item";
    static props = {
        slots: Object,
        size: {
            type: Number,
            optional: true
        }
    };

    setup() {
        if (!this.props.size) {
            this.props.size = 1;
        }
    }
}
