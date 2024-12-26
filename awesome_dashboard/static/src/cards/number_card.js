/** @odoo-module **/

import { Component, xml } from "@odoo/owl";

export class NumberCard extends Component {
    static template = xml`
        <h3 class="text-center"> 
            <t t-esc="props.title"/>
        </h3>
        <h1 class="text-center text-success">
            <t t-esc="props.value"/>
        </h1>
    `;
    static props = {
        title: { type: String },
        value: { type: Number }
    };
}
