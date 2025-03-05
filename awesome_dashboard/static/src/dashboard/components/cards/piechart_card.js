import { Component, xml } from "@odoo/owl";
import { PieChart } from "../pie_chart/pie_chart";


export class PieChartCard extends Component {
    setup(){
        console.log(this.props)
    }
    static template = xml`
        <div class="pie-chart-card">
            <h4><t t-esc="this.props.title"/></h4>
            <PieChart t-props="this.props.data"/>
        </div>
    `;
    static components = { PieChart };
}
