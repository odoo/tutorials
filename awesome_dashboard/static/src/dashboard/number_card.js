import { Component, xml } from '@odoo/owl';

export class NumberCard extends Component {
    static template = xml`
        <p><t t-out="props.title" /></p>
        <div class="o_big-number"><t t-out="props.value" /></div>
    `;

    static props = {
        title: String,
        value: Number
    };
}
