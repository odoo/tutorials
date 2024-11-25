/** @odoo-module **/

import { Component } from "@odoo/owl";

export class AwesomeDashboardNumberCard extends Component {
    static template = "awesome_dashboard.dashboard_number_card";
    static props = {
        title: { type: String, },
        value: { type: Number, }
    }
}
