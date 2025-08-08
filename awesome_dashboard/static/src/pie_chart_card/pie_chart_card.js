import { Component } from "@odoo/owl";
import { PieChart } from "@awesome_dashboard/pie_chart/pie_chart";

export class PieChartCard extends Component {
    static template = "awesome_owl.PieChartCard"
    static components = { PieChart }
    static props = {
        title: {
            type: String,
        },
        values: {
            type: Object,
        }
    }
}
