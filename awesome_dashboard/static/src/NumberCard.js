import {Component, useState, xml} from "@odoo/owl";

export class NumberCard extends Component {
    static template = xml`
        <h5 class="card-title"><t t-esc="props.title" /></h5>
        <p class="card-text">
            <div style="text-align: center;">
                    <t t-esc="props.value" />            
            </div>
        </p>
    `
    static props = {
        value: {type: Number, optional: true},
        title: {type: String, optional: true},
    }
}