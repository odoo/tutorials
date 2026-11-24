import { Component } from "@odoo/owl";

export class NumberCard extends Component {
    static template = "awesome_dashboard.NumberCard";
    static props = {
        title: String,
        value: [Number, String],
        note: { type: String, optional: true },
        color: { type: String, optional: true },
    };
}
