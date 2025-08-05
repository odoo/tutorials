/** @odoo-module **/

import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem";
    static props = {
        size: {
            type: Number,
            optional: true,
        },
        slots: {
            type: Object,
        }
    }

    setup() {
        const size = this.props.size || 1;
        this.width = 18*size;
    }
}
