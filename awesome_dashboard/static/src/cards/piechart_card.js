/** @odoo-module **/

import { Component, xml } from "@odoo/owl";
import { PieChart } from "../piechart/piechart"

export class PieChartCard extends Component {
    static components = { PieChart }
    static template = xml`
        <h3 class="text-center"> 
            <t t-esc="props.title"/>
        </h3>
        <PieChart statistics="props.values"/>
    `;
    static props = {
        title: { type: String },
        values: { type: Object }
    };
}
