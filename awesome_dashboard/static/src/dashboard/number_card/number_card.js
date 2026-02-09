import { Component, xml } from "@odoo/owl";

export class NumberCard extends Component {
    static template = xml`
        <div class="text-center">
            <div class="fs-2 fw-bold" t-esc="props.value"/>
            <div class="text-muted" t-esc="props.title"/>
        </div>
    `;
    static props = ["title", "value"];
}
