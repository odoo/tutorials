/** @odoo-module */

import { Component,xml } from "@odoo/owl";
import { PieChart } from "./pie_chart";

export class PieChartCard extends Component {
    static template = xml`
    <t t-name="awesome_dashboard.PieChartCard" owl="1">
        <t t-esc="props.title"/>
        <PieChart data="props.values" label="''"/>
    </t>`;

    static components = { PieChart }
    static props = {
        title: {
            type: String,
        },
        values: {
            type: Object,
        },
    }
}