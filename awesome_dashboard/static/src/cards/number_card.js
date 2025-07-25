/** @odoo-module **/

import { Component, xml } from "@odoo/owl";

export class NumberCard extends Component {
    static template = xml`
        <div class="card p-3 text-center">
            <h6 class="fw-bold text-primary"> <t t-esc="props.title"/> </h6>
            <div class="fs-1 fw-bold text-success">
                <t t-esc="props.value"/>
            </div>
        </div>
    `;
}
