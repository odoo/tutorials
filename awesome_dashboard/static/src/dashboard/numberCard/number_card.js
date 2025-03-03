import { Component } from "@odoo/owl";

export class NumberCard extends Component {
    static template = "awesome_dashboard.numbercard";
    static props = {
        title: { type: String },
        value: { type: Number },
    };
}
