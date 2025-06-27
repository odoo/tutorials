/** @odoo-module **/

import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static props = {size: {type: Number, default: 1}, slots: {type: Object}}
    static template = "awesome_dashboard.dashboard_item";
}