import { Component, xml } from "@odoo/owl"

import { PieChart } from "../piechart/piechart"

export class PieChartCard extends Component {
    static props = {
        title: { type: String },
        values: { type: Object },
    }

    static components = { PieChart }

    static template = xml`
        <h3 class="card-title text-center">
            <t t-esc="props.title"/>
        </h3>
        <PieChart data="props.values"/>
    `
}
