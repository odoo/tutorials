import { Component, xml } from "@odoo/owl";
import { Item } from "../item/item";
import { PieChart } from "../piechart/piechart";

export class PieChartCard extends Component {
    static components = { Item, PieChart }
    static props = {
        size: { type: Number, optional: true },
        title: { type: String },
        data: { type: Object }
    };
    static defaultProps = {
        size: 1,
    };
    static template = xml`
        <Item size="props.size">
            <h5 t-esc="this.props.title" />
            <PieChart data="this.props.data"/>
        </Item>`;
}
