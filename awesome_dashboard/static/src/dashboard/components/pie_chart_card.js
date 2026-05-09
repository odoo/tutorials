import { Component } from "@odoo/owl"
import { PiChart } from "../chart/piChart";

export class PieChartCard extends Component {
    static template = "awesome_dashboard.PieChartCard";
    static components = { PiChart }

    static props = {
        title: String,
        data: Object
    }
}
