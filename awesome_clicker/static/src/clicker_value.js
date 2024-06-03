/** @odoo-module **/
import { Component, useState, xml } from "@odoo/owl";
import { humanNumber } from "@web/core/utils/numbers";
import { useClicker } from "./clicker_service";


export class ClickerValue extends Component {
    setup() {
        this.state = useClicker();
    }

    formattedValue() {
        return humanNumber(this.state.count || 0, { decimals: 1, minDigits: 1 });
    }
}

ClickerValue.template = xml`
<span t-att-data-tooltip="state.count">
    <t t-esc="formattedValue()"/>
</span>
`;