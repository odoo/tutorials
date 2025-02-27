/** @odoo-module **/

import { Component } from "@odoo/owl";
import { PieChart } from "../piechart/piechart";

export class PieCard extends Component {
    static template = "awesome_dashboard.PieCard";
    static components = { PieChart }
    static props = {
        title : { type : String },
        value : { type : Object }
    }
}
