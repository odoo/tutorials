import { Component, xml } from "@odoo/owl";
import { PieChart } from "./piechart";

export class PieChartCard extends Component {
    static props = {
        title: { type: String },
        value: { type: Object },
    };
    static components = { PieChart };
    static template = xml`
        <t t-name="awesome_dashboard.PieChartCard">
            <t t-esc="props.title"/>
            <PieChart data="props.values"/>
        </t>
    `
}