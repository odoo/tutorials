/** @odoo-module */

import { Component, useState } from '@odoo/owl';
import { Counter } from '../counter/counter';

export class Card extends Component {
    static template = 'awesome_owl.Card';
    static components = { Counter };
    static props = {
        title: { type: String },
        content: { type: String },
        incrementsum: { type: Function },
    };
    setup() {
        this.state = useState({ isOpen: true });
        this.toggleView = this.toggleView.bind(this);
    }
    toggleView() {
        this.state.isOpen = !this.state.isOpen;
    }
}
