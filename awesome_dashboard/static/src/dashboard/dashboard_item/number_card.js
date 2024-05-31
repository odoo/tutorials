/** @odoo-module **/

import { Component, xml } from "@odoo/owl";

export class NumberCard extends Component {
}

NumberCard.template = xml`
    <h5><t t-esc="props.title"/></h5>
    <div class="text-success h3 w-100 text-center" t-esc="props.value"/>
`;
NumberCard.props = {
    title: { type: String },
    value: { type: Number },
};
