import { Component, xml } from "@odoo/owl";

export class TextCard extends Component {
    static template = xml`<p><t t-esc="props.title"/></p><h3 class="text-success"><t t-esc="props.value"/></h3>`;
    static props = {
        title: String,
        value: String,
    };
}