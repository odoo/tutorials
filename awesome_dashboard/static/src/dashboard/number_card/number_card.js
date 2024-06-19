/** @odoo-module **/

import { Component } from "@odoo/owl";

export class NumberCard extends Component {
    static template = "awesome_dashboard.components.number_card";
    static props = {
        title: { type: Number, optional: true, default: 1 },
        value: Number,
    };
}
