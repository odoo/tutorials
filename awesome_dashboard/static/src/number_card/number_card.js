import { Component } from "@odoo/owl";

export class NumberCard extends Component {
    static template = "awesome_dashbaord.number_card"

    static props = {
        title: {
            type: String,
            optional: true
        },
        value: {
            type: Number,
            optional: true,
            default: 0
        }
    }
}
