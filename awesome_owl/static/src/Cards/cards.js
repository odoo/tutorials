/** @odoo-module **/

import { Component, useState} from '@odoo/owl';
import { markup } from '@odoo/owl';

export class Card extends Component {
    static template = "awesome_owl.Card"; 
    static props = {
        title: { type: String },
        slots: {
            type: Object,
            shape: {
              default: true,
            },
        },
    };

    setup() {
        this.state = useState({ isOpen: true });
    }

    toggleContent() {
        this.state.isOpen = !this.state.isOpen;
    }

    get processedContent() {
        return markup(this.props.content);
    }
}
