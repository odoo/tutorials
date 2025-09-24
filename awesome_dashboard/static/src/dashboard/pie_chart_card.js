import { Component, xml } from "@odoo/owl";
import { PieChart } from "./pie_chart/pie_chart";

export class PieChartCard extends Component {
    static components = { PieChart };
    static props = {
        title: String,
        value: Object,
    };

    static template = xml`
        <p><t t-esc="props.title" /></p>
        <PieChart data="props.value" /> 
    `;
}
