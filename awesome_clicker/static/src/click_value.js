import { Component, xml } from "@odoo/owl";
import { humanNumber } from "@web/core/utils/numbers";

export class ClickValue extends Component {
    static props = {
        value: Number,
    };
    static template = xml`<t t-esc="format(props.value)"/>`;

    format(value) {
        if (value < 1000) {
            return value;
        } else {
            return humanNumber(value, { minDigits: 0, decimals: 1 });
        }
    }
}
