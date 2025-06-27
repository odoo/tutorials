/** @odoo-module **/

import { Component } from "@odoo/owl";
import {PieChart} from "./pie_chart";

export class PieChartCard extends Component {
    static components = {PieChart}
    static template = "awesome_dashboard.pie_chart_card";
    static props = {
        title: {type: String},
        values: {type: Object},
    };
}