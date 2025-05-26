
import { Component, useState, xml } from "@odoo/owl";

export class Card extends Component {
    static template = xml`<div class="card d-inline-block m-2">
            <h5 class="card-title"><t t-esc="state.title"/></h5>
            <p class="card-text"><t t-esc="state.content"/></p>
        </div>`;

    setup() {
        this.state = useState({title:  this.props.title, content:this.props.content})
    }

}