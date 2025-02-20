/** @odoo-module **/

import { Component, markup } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card_template";
    static props = {
        title: { type: String },
        content: { type: String },
    };

    get safeContent() {
        return markup(this.props.content);
    }
}
