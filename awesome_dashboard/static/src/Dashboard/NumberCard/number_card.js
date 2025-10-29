/** @odoo-module alias=@awesome_dashboard/NumberCard/number_card default=false**/

import { Component } from "@odoo/owl";

export class NumberCard extends Component {
    static template = "awesome_dashboard.NumberCard";
    static props = {
        title: {
            type: String,
        },
        value: {
            type: Number,
        }
    }
}
