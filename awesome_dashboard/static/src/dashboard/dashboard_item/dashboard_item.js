/** @odoo-module **/

import {Component} from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem";
    static props = {
        title: String,
        slots: Object,
        size: {
            type: Number,
            optional: true,
        }
    };

    static defaultProps = {
        size: 1,
    }
}