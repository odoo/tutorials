import { Component } from "@odoo/owl"

// Component representing a single dashboard item
export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem"

    // Definition of expected component properties
    static props = {
        slots: {
            type: Object,
            shape: {
                default: Object
            }
        },
        size: {
            type: Number,
            optional: true // Size is optional and defaults to 1 if not provided
        },
    };
}
