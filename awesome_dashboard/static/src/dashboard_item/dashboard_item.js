/** @odoo-module */

import { Component } from "@odoo/owl";

export class AwesomeDashboardItem extends Component {
    static template = "awesome_dashboard.dashboard_item";
    static props = { 
        slots: {
            type: Object,
            shape: {
                default: Object
            },
        },
        size: {
            type: Number,
            default:1,
            optional:true
        },
    };
}
