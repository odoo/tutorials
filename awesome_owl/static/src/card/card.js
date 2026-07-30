import { Component, xml } from "@odoo/owl";


export class Card extends Component {
    static template = xml`
        <div class="card d-inline-block m-2" style="width: 18rem;">
            <div class="card-body">
                <h5 class="card-title" t-esc="props.title" />
                <p class="card-text" t-esc="props.content" />
            </div>
        </div>
    `;

    static props = {
        title: String,
        content: String,
    }
}
