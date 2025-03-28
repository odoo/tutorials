/** @odoo-module **/

import { Component, xml, onMounted } from "@odoo/owl";
import { PieChart } from "./pie_chart";

export class PieChartCard extends Component {
    static components = { PieChart };
    static template = xml`
        <div>
            <h1 t-esc="props.title"></h1>
            <PieChart t-props="{data: props.data}" />
        </div> 
    `;
    static props = {
        title: String,
        data: Object,
    };
}
