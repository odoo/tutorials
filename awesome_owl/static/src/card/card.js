/** @odoo-module **/
import { Component, useState } from "@odoo/owl"

export class Card extends Component {
    static template = 'awesome_owl.Card'
    setup() {
        this.state = useState({ contentVisible: true });
    }

    onToggleContent() {
        this.state.contentVisible = !this.state.contentVisible;
    }
}