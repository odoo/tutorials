/** @odoo-module **/

import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem";
    static props = {
        slot: { type: Object, optional: true },
        size: { type: Number, optional: true },
    };

    static defaultProps = {
        size: 1
    }
}
