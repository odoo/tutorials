
import { Component, useState, xml } from "@odoo/owl";

export class Card extends Component {
    static template = xml`
<div class="card d-inline-block m-2">
    <div class="card-header">
        <button class="btn btn-primary" t-on-click="() => state.state=!state.state">Toggle</button>
    </div>
    <div t-if="state.state">
        <h5 class="card-title"><t t-esc="state.title"/></h5>
        <p class="card-text">
            <t t-slot="default"/>
        </p>
    </div>
</div>`;
    static props = {
        title: String,
        slots: {
            type: Object,
            shape: {
                default: true
            },
        }
    }

    setup() {
        this.state = useState({ title: this.props.title, state: true})
    }

    toggle() {

    }
}
