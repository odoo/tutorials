/** @odoo-module **/

import { Component, xml } from "@odoo/owl";
import { PieChart } from "./pie_chart/pie_chart";

export class PieChartCard extends Component {
    static components = { PieChart }

    static props = {
        label: String,
        data: Object,
    }

    static template = xml`
        <div>
            <t t-esc="props.label"/>
        </div>
        <div>
            <PieChart data="props.data" label="props.label"/>
        </div>
    `;
}
