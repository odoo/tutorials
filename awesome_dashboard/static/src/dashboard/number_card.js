import { Component, xml } from "@odoo/owl";

export class NumberCard extends Component {
    static props = {
        title: String,
        value: { optional: true },
    };
    
    static template = xml`
    <t t-name="awesome_dashboard.NumberCard">
    <div class="d-flex flex-column align-items-center">
        <h3 t-out="props.title" class="text-muted"/>
        <div class="display-1" t-out="props.value"/>
    </div>
    </t>`;
}
