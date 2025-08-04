/** @odoo-module **/

import { Component, xml } from "@odoo/owl";

export class NumberCard extends Component {
    static props = {
        label: String,
        value: Number,
    }

    static template = xml`
        <div>
            <t t-esc="props.label"/>
        </div>
        <div class="text-success text-center">
            <t t-esc="props.value"/>
        </div>
    `;
}
