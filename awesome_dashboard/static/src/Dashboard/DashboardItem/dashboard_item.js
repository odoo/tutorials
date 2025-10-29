/** @odoo-module alias=@awesome_dashboard/DashboardItem/dashboard_item default=false**/

import { Component } from "@odoo/owl"

export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem"
    static props = {
        size: {
            type: Number,
            optional: true,
            default: 1
        },
        slots: {
            type: Object,
            shape: {
                default: Object
            }
        },
    }
}
