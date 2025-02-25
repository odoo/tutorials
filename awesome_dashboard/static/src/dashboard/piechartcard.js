/** @odoo-module **/
import { Component, xml } from "@odoo/owl";
import { PieChart } from "./piechart";

export class PieChartCard extends Component {
    static template = xml` <PieChart></PieChart> `;
    static components = { PieChart }
}
