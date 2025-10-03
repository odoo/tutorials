import { Component, xml, useState } from '@odoo/owl';
import { useClicker } from './clicker_hook';
import { humanNumber } from "@web/core/utils/numbers";

export class ClickValue extends Component {
    static template = xml`<span t-att-data-tooltip="clicker.state.clicks"><t t-esc="get_value"/></span>`;
    setup() {
        this.clicker = useClicker();
    }

    get get_value() {
        return humanNumber(this.clicker.state.clicks, { decimals: 1 });
    }

}
