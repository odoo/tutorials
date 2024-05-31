/** @odoo-module **/

import { Component, xml } from "@odoo/owl";
import { PieChart } from "../piechart/piechart";

export class PieChartCard extends Component {
}

PieChartCard.template = xml`
    <h5><t t-esc="props.title"/></h5>
    <PieChart data="props.value" />
`;
PieChartCard.props = {
    title: { type: String },
    value: { type: Object },
};
PieChartCard.components = { PieChart };