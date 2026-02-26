import { Component, xml } from "@odoo/owl";


export class NumberCard extends Component {
    static template = xml`
        <div class="card-body text-center">
            <t t-esc="props.title"/>
            <div class="text-success h2 mt-3">
                <t t-esc="props.value"/>
            </div>
        </div>
    `
    static props = {
        title: { type: String, required: true },
        value: { type: Number, required: true },
    }
}
