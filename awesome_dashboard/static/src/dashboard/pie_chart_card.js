/** @odoo-module **/

import {Component} from "@odoo/owl"

import { PieChart } from "./piechart"

export class PieChartCard extends Component {

    static template = "awesome_dashboard.PieChartCard";

    static components = {PieChart};

    static props = {
        title: String,
        values: Object,
    };
}
