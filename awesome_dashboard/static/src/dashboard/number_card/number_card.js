// imports
import { Component } from "@odoo/owl";


export class NumberCard extends Component {
    // used to display numerical data with a title
    static template = "awesome_dashboard.NumberCard";
    static props = {
        title: {
            type: String,
        },
        value: {
            type: Number,
        }
    };
}
