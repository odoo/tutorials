import { Component, xml } from "@odoo/owl";
import { PieChart } from "../piechart/piechart";

export class PieChartCard extends Component {
    static template = xml`
        <div class="dashboard-piechart-class">
            <h3><t t-esc="props.title"/></h3>
            <PieChart data="props.data"/>
        </div>
    `;
    static components = { PieChart };
    static props ={
        title : String,
        data : Object,
    };
}
