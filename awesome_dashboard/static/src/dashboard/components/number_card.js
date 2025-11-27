/** @odoo-module **/

import { Component, xml } from "@odoo/owl";

export class NumberCard extends Component {
    static template = xml`
        <div class="dashboard-card number-card">
            <h3 t-esc="props.title"/>
            <span t-esc="props.value" class="number-value"/>
        </div>
    `;
    static props = {
        title: String,
        value: Number,
    };
}
