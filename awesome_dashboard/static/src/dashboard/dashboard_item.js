import { Component } from "@odoo/owl";

export class AwesomeItem extends Component {
    static template = "awesome_dashboard.DashboardItem";
    static props = {
        "title": String, 
        "value": { type: [String, Number], optional: true },
        "size": { type: Number, optional: true }, 
        "slots": { type: Object, optional: true },
    };

    get cardWidth() {
        // Calculate width based on a 4-column grid system, accounting for gaps
        const size = this.props.size || 1;
        // For a container with gaps, we need to calculate the available space
        // 25% per column, minus proportional gap space
        const columnWidth = 25;
        const gapAdjustment = 1.2; // Small adjustment for gaps
        return `calc(${size * columnWidth}% - ${gapAdjustment}rem)`;
    }
}
