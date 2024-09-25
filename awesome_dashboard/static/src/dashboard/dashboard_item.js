/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.dashboard_item";
    static props = {
        size: {type: Number, optional: true, default: 1},
        slots: {type: Object}

    };

}
