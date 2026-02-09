import { Component, xml } from "@odoo/owl";
import { PieChart } from "../pie_chart/pie_chart";

export class PieChartCard extends Component {
    static components = { PieChart };
    static template = xml`
        <PieChart data="props.data" label="props.label"/>
    `;
    static props = ["data", "label"];
}
