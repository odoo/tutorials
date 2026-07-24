import { Component } from "@odoo/owl";

export class NumberCard extends Component {
    static template = "awesome_dashboard.NumberCard";
    static props = {
        size: {
            type: Number,
            default: 1,
            optional: true,
        },
        title: {type: String},
        value: {type: String},
        slots: {
            type: Object,
        }
    }
}