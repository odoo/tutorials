/** @odoo-module **/

import { Component, xml } from "@odoo/owl";
import { PieChart } from "../pie_chart/pie_chart";

export class PieChartCard extends Component {
    static template = xml`
        <t t-out="props.title"/>
        <PieChart data="props.data"/>
    `;
    static components = { PieChart }

    static props = {
        data: {
            type: Object
        }
    };
}
