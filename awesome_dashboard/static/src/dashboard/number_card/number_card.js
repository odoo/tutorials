import { Component } from "@odoo/owl";

// Displays a numeric value with title and optional formatting
export class NumberCard extends Component {
    static template = "awesome_dashboard.NumberCard";
    static props = {
        title: {
            type: String,
        },
        value: {
            type: Number,
        },
        icon: {
            type: String,
            optional: true,
        },
        color: {
            type: String,
            optional: true,
            validate: color => ["primary", "success", "info", "warning", "danger", "secondary"].includes(color)
        },
        prefix: {
            type: String,
            optional: true,
        },
        suffix: {
            type: String,
            optional: true,
        }
    }
}
