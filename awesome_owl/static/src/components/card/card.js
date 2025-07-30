import { Component, markup } from '@odoo/owl'

export class Card extends Component {
    static template = "awesome_owl.Card"
    static components = {}
    static props = {
        title: { type: String, default: "Card Title" },
        body: { type: String, default: "Card Body" },
        visit: { type: String, default: "Visit us", optional: true }
    }

    setup() {
        super.setup();
        this.markup_visit = markup(this.props.visit)
    }
}
