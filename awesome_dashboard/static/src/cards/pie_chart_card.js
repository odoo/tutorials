/** @odoo-module **/

import { Component, xml } from "@odoo/owl";
import { PieChart } from "../dashboard/pie_chart/pie_chart"; 

export class PieChartCard extends Component {
    static template = xml`
        <div class="d-flex flex-column align-items-center">
            <div class="fw-bold"><t t-esc="props.title"/></div>
            <PieChart data="props.data"/>
        </div>
    `;
    static components = { PieChart };
}
