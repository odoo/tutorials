import { Component, xml } from "@odoo/owl";


export class NumberCard extends Component {
    static template = xml`
        <t t-esc="props.title"/>
        <div class="fs-1 fw-bold text-success text-center">
            <t t-esc="props.value"/>
        </div>
    `;

    static props = {
        title: {type: String},
        value: {type: String}
    }
}

