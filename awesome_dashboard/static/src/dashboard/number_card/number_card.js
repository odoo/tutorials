/** @odoo-module **/

import { Component } from "@odoo/owl";

export class NumberCard extends Component {
    static template = "awesome_dashboard.NumberCard";
    static props = {
        title: { type: String, optional: true, default: 1 },
        value: Number,
    };
}
