import { Component, markup, useState } from '@odoo/owl'

export class Card extends Component {
    static template = "awesome_owl.Card"
    static components = {}
    static props = {
        title: { type: String, default: "Card Title", required: true },
        slots: { type: Object },
        visit: { type: String, default: "Visit us", optional: true }
    }

    setup() {
        super.setup();
        this.state = useState({ isOpen: true })
        this.markup_visit = markup(this.props.visit)
    }

    toggleCard() {
        this.state.isOpen = !this.state.isOpen;
    }
}
