/** @odoo-module **/

import { Component} from "@odoo/owl";
export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem"
    
    static props = {
            value:Number,
        slots: {
            type: Object,
            shape: {
                default: Object
            },
        },
        size: {
            type: Number,
            default: 1,
            optional: true,
        },
    };
}