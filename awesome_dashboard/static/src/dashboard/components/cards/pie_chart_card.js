import { Component, xml } from "@odoo/owl";
import { PieChart } from "../Pie_chart/Pie_chart";

export class PieChartCard extends Component {
  static template = xml`
        <div class="pie-chart-card">
            <h4><t t-esc="props.title"/></h4>
            <PieChart t-props="props.data"/>
        </div>
    `;
  static components = { PieChart };
}
