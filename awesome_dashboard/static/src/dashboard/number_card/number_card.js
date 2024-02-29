/** @odoo-module **/

import { Component, xml } from "@odoo/owl";

export class NumberCard extends Component {
    static template = xml`
        <t t-out="props.title"/>
        <h2>
            <t t-out="props.value"/>
        </h2>
    `;

    static props = {
        title: String,
        value: Number
    };
}
