import { Component, xml } from "@odoo/owl"

export class NumberCard extends Component {
    static props = {
        title: { type: String },
        value: { type: [Number, String] },
    }

    static template = xml`
        <h3 class="card-title text-center">
            <t t-esc="props.title"/>
        </h3>
        <span class="fs-1 text-center text-primary">
            <t t-esc="props.value"/>
        </span>
    `
}
