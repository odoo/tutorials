import { Component, xml } from "@odoo/owl";
import { PieChart } from "./pie_chart";


export class PieCard extends Component {
    static components = { PieChart };
    static template = xml`
        <div class="card-body text-center">
            <t t-esc="props.title"/>
            <PieChart data="props.value"/>
        </div>
    `
    static props = {
        title: { type: String, required: true },
        value: { type: Number, required: true },
    }
}
