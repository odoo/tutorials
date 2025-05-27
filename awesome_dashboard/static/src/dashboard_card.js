/** @odoo-module **/

import { Component, xml } from "@odoo/owl";

export class DashboardCard extends Component {
    static template = xml`
        <div 
            class="card d-inline-block m-2" 
            t-att-style="'width: ' + (18 * props.size) + 'rem; padding: 12px;'"
        >
            <t t-slot="content"/>

            <div style="color: green; font-size: 28px; display: flex; justify-content: center; align-items: center;">
                <t t-esc="props.value"/>
            </div>
        </div>
    `

    static props = {
        size: { type : Number},
        value: { type : Number},
        slots: {
            type: Object,
            optional: true
        }
    };
}

