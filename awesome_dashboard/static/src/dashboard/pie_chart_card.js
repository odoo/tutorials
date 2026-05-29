import { Component, xml } from "@odoo/owl";
import { PieChart } from "./pie_chart";

export class PieChartCard extends Component {
    static props = {
        data: Object
    }

    static components = { PieChart };

    static template = xml`
    <t t-name="awesome_dashboard.PieChartCard">
        <div class="d-flex flex-column align-items-center">
            <h3 t-out="props.title" class="text-muted"/>
            <PieChart data="props.data"/>
        </div>
    </t>`;
}
