/** @odoo-module **/

import { Component, markup } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";

    static props = {
        title: {
            type: String,
            optional: true,
        },
        content: {
            type: String,
            optional: true,
        },
    };

    get content() {
        if (this.props.content) {
            return markup(this.props.content);
        }
        return undefined;
    }
}
