/** @odoo-module **/

import { Component } from "@odoo/owl";
import { PieChart } from "../pie_chart/pie_chart";

export class Piecard extends Component {
    static template = "awesome_dashboard.pie_chart_card";
    static components = { PieChart }
    static props = {
        itemProps: { type: Object, elements: { title: String, value: Number } }
    }
}
