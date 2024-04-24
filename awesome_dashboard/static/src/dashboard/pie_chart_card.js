/** @odoo-module **/

import { Component } from "@odoo/owl";
import { PieChart } from "./pie_chart";


export class PieChartCard extends Component {
    static template = "awesome_dashboard.PieChartCard";
    static components = { PieChart };
    static props = {
        title: {type: Number,}
        ,value: {type: Object},
    };
    
}