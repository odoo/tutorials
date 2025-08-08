import { Component, xml } from "@odoo/owl";
import { PieChart } from "../pieChart";

export class PieChartCard extends Component {
    static template = xml`
        <PieChart label="props.label" data="props.data"/>
    `;
    static components = { PieChart }
    
    static props = {
        label: {type: String},
        data: {type: Object}
    }
}

