import { Component } from "@odoo/owl";

export class NumberCard extends Component {
    static template = "awesome_dashboard.number-card";
    static props = {
        title: String,
        value: Number,
    };
}
