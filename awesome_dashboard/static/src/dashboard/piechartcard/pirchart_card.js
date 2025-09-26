import { Component } from "@odoo/owl";
import { PieChart } from "../pie_chart/pie_chart";

export class PieChartCard extends Component {
    static components = { PieChart }
    static template = "awesome_dashboard.piechartcard";
    static props = {
        title: {
            type: String,
        },
        data: {
            type: Object,
        },
    };
}

