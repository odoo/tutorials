/** @odoo-module **/

import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem";
    static props = {
        size: {
            type: Number,
        },
        slots: {type: Object},
    };
    static defaultProps = {
        size: 1,
    };

}