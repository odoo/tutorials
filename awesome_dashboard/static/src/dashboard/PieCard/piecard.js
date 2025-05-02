import {Component,xml} from "@odoo/owl"
import { PieChart } from "../pie/pie"

export class PieCard extends Component{
    static template=xml`
    <div class="dashboard-card">
    <t t-esc="props.title"/>
    <PieChart t-props="props.data"/>
    </div>
    `
    static components={PieChart}
}