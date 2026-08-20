import { Component, xml, useState } from "@odoo/owl"

export class Card extends Component {
    static props = {
        title: String,
        slots: { type: Object, optional: true },
    }

    setup() {
        this.state = useState({isOpen: false});
    }

    handleToggle() {{
        this.state.isOpen = !this.state.isOpen;
    }}


    static template = xml`
        <div class="card d-inline-block m-2" style="width: 18rem;">
            <div class="card-body">
                <div class="d-flex justify-content-between mb-1">
                    <h5 class="card-title">
                        <t t-esc="props.title"/>
                    </h5>
                    <button t-on-click="handleToggle">Toggle</button>
                </div>
                <div t-if="state.isOpen" class="card-text">
                    <t t-slot="default"/>
                </div>
            </div>
        </div>
    `
}