/** @odoo-module **/

import {Component} from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.dashboard_item"
    static porps = {
        slots: {},
        size: {
            type: Number,
            optional: true,
        },
        title: String,
    }
    static defaultProps = {
        size: 1,
    };
}