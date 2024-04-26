/** @odoo-module **/

import { Component, xml } from "@odoo/owl";
import { humanNumber } from "@web/core/utils/numbers";

export class ClickValue extends Component {
    static template = xml`<span t-att-data-tooltip="props.clicks"><t t-esc="getFormattedClicks()"/></span>`;

    static props = {
        clicks: Number
    }

    getFormattedClicks() {
        return humanNumber(this.props.clicks, { decimals: this.props.clicks > 1000, minDigits: 1 })
    }
}
