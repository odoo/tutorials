import { Component, xml } from "@odoo/owl";
import { PieChart } from "../pie_chart/pieChart";

export class PieChartCard extends Component {
    static template = xml`<p><t t-esc="props.title"/></p><PieChart data="props.data" label="props.label"/>`;
    static components = { PieChart };
    static props = {
        title: String,
        label: String,
        data: Object,
    };
}