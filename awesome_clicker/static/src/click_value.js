import { Component, xml } from "@odoo/owl";
import { humanNumber } from "@web/core/utils/numbers";

export class ClickValue extends Component {
    static props = {
        label: { type: String, optional: true },
        icon: { type: String, optional: true },
        value: Number,
    };
    static template = xml`
        <span t-att-data-tooltip="props.value">
            <t t-esc="props.label || ''"/>
            <t t-esc="format(props.value)"/>
            <i t-if="props.icon" class="fa fa-fw" t-att-class="props.icon"/>
        </span>
        `;

    format(value) {
        if (value < 1000) {
            return value;
        } else {
            return humanNumber(value, { minDigits: 0, decimals: 1 });
        }
    }
}
