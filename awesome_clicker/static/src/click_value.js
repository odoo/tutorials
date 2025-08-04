/** @odoo-module **/

import { Component } from "@odoo/owl";
import { humanNumber } from "@web/core/utils/numbers";

export class ClickValue extends Component {
    static template = "awesome_clicker.ClickValue";
    static props = {
        value: { type: Number },
    };

    get formattedValue() {
        return humanNumber(this.props.value, { decimals: 1 });
    }

    get tooltipText() {
        return this.props.value.toLocaleString();
    }
}
