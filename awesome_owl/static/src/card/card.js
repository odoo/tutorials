import { Component, xml, useState } from "@odoo/owl";

export class Card extends Component {
    static template = xml`
        <div class="card d-inline-block m-2" style="width: 18rem;">
            <div class="card-body">
                
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h5 class="card-title mb-0"><t t-esc="props.title"/></h5>
                    <button class="btn btn-sm btn-outline-primary" t-on-click="toggle">
                        <t t-if="state.isOpen">Hide</t>
                        <t t-else="">Show</t>
                    </button>
                </div>
                
                <div t-if="state.isOpen">
                    <t t-slot="default"/>
                </div>
                
            </div>
        </div>
    `;

    static props = {
        title: { type: String },
        slots: { type: Object, optional: true }
    };

    setup() {
        this.state = useState({
            isOpen: true
        });
    }

    toggle() {
        this.state.isOpen = !this.state.isOpen;
    }
}
