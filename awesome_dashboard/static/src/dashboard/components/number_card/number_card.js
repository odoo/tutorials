import { Component } from "@odoo/owl";

export class NumberCard extends Component {
    static template = "awesome_dashboard.NumberCard";
    static props = {
        label: String,
        value: [Number, String],
    };
}