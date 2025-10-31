import {Component} from "@odoo/owl";
import { humanNumber } from "@web/core/utils/numbers";

export class ClickValue extends Component {
    static template = 'awesome_clicker.click_value'
    static props = { value: Number }
    static components = {}

    setup() {}

    humanizedValue() {
        return humanNumber(this.props.value);
    }
}