import { Component, xml } from "@odoo/owl";
import { Item } from "../item/item";

export class NumberCard extends Component {
    static components = { Item };
    static props = {
        size: { type: Number, optional: true },
        title: { type: String },
        value: { type: Number }
    };
    static defaultProps = {
        size: 1,
    };

    static template = xml`
        <Item size="props.size">
            <h5 t-esc="this.props.title" />
            <p t-esc="this.props.value" />
        </Item>`;
}
