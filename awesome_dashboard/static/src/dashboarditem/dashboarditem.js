/** @odoo-module **/

import { Component } from "@odoo/owl";


export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem";
    static props = {
        size: { type: Number, optional: true },
        slots: { type: Object }
    }
    setup() {
        this.defaultSize = this.props.size ?? 1;
    }
}
