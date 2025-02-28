import { Component, useEffect, xml } from "@odoo/owl";

import { humanNumber } from "@web/core/utils/numbers";

import { useClicker } from "./clicker_service";

export class ClickValue extends Component {
    static template = xml`<p>Clicks: <span t-att-data-tooltip="clicker.clicks"><t t-esc="text"/></span></p>`;
    static props = {};

    setup() {
        this.clicker = useClicker();
    }

    get text() {
        return humanNumber(this.clicker.clicks);
    }
}
