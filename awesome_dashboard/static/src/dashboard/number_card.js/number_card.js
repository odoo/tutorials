import { Component } from "@odoo/owl";

export class NumberCard extends Component {
    static template = "awesome_dashboard.NumberCard";
    static props = {
        title: {
            type: String,
            optional: false,
        },
        value: {
            type: Number,
            optional: false,
        },
    }
}