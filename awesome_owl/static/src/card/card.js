/** @odoo-module **/

import { Component, xml } from "@odoo/owl"

export class Card extends Component {
    static props = {
        title: String,
        content: String
    }

    static template = xml`
        <div class="card d-inline-block m-2" style="width: 18rem;">
        <div class="card-body">
        <t t-log="props"/>
        <h5 class="card-title"><t t-out="props.title"/></h5>
            <p class="card-text">
                <t t-out="props.content"/>
            </p>
        </div>
        </div>
    `;
}