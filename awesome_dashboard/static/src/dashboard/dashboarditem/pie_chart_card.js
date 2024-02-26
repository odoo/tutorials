/** @odoo-module **/

import { Component } from "@odoo/owl";
import {PieChart} from "../piechart/piechart"


export class PieChartCard extends Component {
    static template = "awesome_dashboard.PieChartCard"
    static props = {
        title : {
            type: String
        },
        values: {
            type: Object
        }
    };
    static components = {PieChart};
}
