/** @odoo-module **/

import { Component } from "@odoo/owl";

export class AwesomeDashboardItem extends Component {
    static template = "awesome_dashboard.dashboard_item";
    static props = {
        size: {
            type: Number,
            optional: true,
        },
        slots: {
            type: Object,
            optional: true,
        },
    }
}
