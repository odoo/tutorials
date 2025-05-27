/** @odoo-module **/

import { Component } from "@odoo/owl";

export class NumberCard extends Component {
    static template = "awesome_dashboard.NumberCard";
    static props = {
        title: { type: String, optional: true },
        value: { type: [String, Number] },
    };
}
