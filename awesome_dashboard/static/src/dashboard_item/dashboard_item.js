/** @odoo-module **/

import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem";

    static props = {
        size: {type: Number, default: 1},
    };
}
