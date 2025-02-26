import { Component } from "@odoo/owl";

// NumberCard component to display a numeric value with a title
export class NumberCard extends Component {
    static template = "awesome_dashboard.NumberCard";

    // Props expected by the component
    static props = {
        title: {
            type: String, // Title of the number card
        },
        value: {
            type: Number, // Numeric value to display
        }
    };
}
