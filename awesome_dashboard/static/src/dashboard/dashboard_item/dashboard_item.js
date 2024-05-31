/** @odoo-module **/

import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    setup() {
        this.size = this.props.size || 1;
        this.slots = this.props.slots;
    }
}

DashboardItem.template = "awesome_dashboard.DashboardItem";
DashboardItem.props = {
    size: { type: Number, optional: true },
    slots: { type: Object, optional: true },
};