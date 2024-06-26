/** @odoo-module **/

import { Component } from "@odoo/owl";

export class NumberCard extends Component {
    static template = "awesome_dashboard.number_card";
    static props = {
        title: String,
        value: Number,
    }
}
