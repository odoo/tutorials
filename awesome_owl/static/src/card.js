import { Component, xml } from "@odoo/owl"

export class Card extends Component {
    static template = xml`
    <div class="card d-inline-block m-2" style="width: 18rem;">
    <div class="card-body">
        <h5 class="card-title"><t t-esc="props.title"/></h5>
        <p class="card-text">
         <t t-out="props.content"/>
        </p>
    </div>
</div>
    `;
    static props = {
        title: { type: String },
        content: { type: [Object, String] },
    }
}
