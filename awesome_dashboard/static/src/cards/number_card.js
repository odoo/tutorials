/** @odoo-module **/

import { Component, xml } from "@odoo/owl";

export class NumberCard extends Component {
    static props = {
        title: String,
        value: Number
    }

    static template = xml`
    <div>
        <h4 class="text-center"><t t-out="props.title"/></h4>
        <h1 class="text-success text-center">
            <t t-out="props.value"/>
        </h1>
    </div>
    `
}
