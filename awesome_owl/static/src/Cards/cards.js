/** @odoo-module */

import { Component } from '@odoo/owl';
import { markup } from '@odoo/owl';

export class Card extends Component {
    static template = "awesome_owl.Card"; 
    static props = {
        title: { type: String },
        content: { type: String },
    };

    get processedContent() {
        return markup(this.props.content);
    }
}
