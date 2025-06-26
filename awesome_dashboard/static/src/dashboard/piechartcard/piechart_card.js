/** @odoo-module **/

import { Component, useRef, onMounted } from "@odoo/owl";
import { PieChart } from "../piechart/pie_chart";

export class PieChartCard extends Component {
    static template = "awesome_dashboard.PieChartCard";
    static components = { PieChart }

    static props = {
        title: { type: String, optional: false },
        chartData: { type: Object, optional: false },
    };

}
