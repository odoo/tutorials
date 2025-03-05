import { Component, xml } from "@odoo/owl";


export class NumberCard extends Component {
    static template = xml`
        <div class="number-card">
            <h4><t t-esc="props.title"/></h4>
            <h1 class="text-success"><t t-esc="props.value"/></h1>
        </div>
    `;
}
