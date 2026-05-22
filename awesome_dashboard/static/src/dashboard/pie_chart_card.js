import { Component, xml } from "@odoo/owl";
import { PieChart } from "./pie_chart";

export class PieChartCard extends Component {
    static template = xml`<div>
	  <p class="font-weight-bold"><t t-out="props.title"/></p>
	  <PieChart data="props.value" />
  </div>`;
    static components = { PieChart };
}
