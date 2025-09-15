/** @odoo-module */

import { Component } from "@odoo/owl";
import { PieChart } from "../pie_chart/pie_chart";

export class PieCard extends Component {
    static template = "awesome_dashboard.PieCard";
    static components = { PieChart }
    static props = {
        title: {
            type: String,
        },
        values: {
            type: Object,
        },
    }
}
