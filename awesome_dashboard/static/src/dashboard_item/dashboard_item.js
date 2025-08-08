/** @odoo-module **/

import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.dashboard_item";
    static props = {
        slots: {
            type: Object,
            shape: {
                defualt: Object
            },
        },
        size: {
            type: Number,
            optional: true,
        }
    };
}
