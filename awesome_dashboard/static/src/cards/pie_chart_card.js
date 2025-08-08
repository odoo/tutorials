/** @odoo-module **/

import { Component, xml } from "@odoo/owl";
import { PieChart } from "../piechart/piechart";

export class PieChartCard extends Component {
    static props = {
        title: String,
        value: Object
    }
    static components = { PieChart }

    static template = xml`
    <div>
        <h4 class="text-center"><t t-out="props.title"/></h4>        
        <PieChart t-props="props.value"/>
    </div>
    `
}
