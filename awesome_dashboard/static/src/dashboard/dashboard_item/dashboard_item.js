/** @odoo-module **/

import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem";
    static props = {
        title: { type: String, optional: true },
        size: { type: Number, optional: true },
        slots: { type: Object, shape: { default: true } },
    };
    static defaultProps = {
        size: 1,
    };
}
