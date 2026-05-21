import { Component } from "@odoo/owl";

export class NumberCard extends Component {
    static template = "numberCard"

    static props = {
        title: { type: String },
        value: { type: Number }
    }
}