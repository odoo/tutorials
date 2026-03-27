import { Component, useState, markup } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        title: String,
        onCardClick: Function,
        slots: {type: Object, optional: true}
    }
    
    setup() {
        this.clicks = useState({ value: 0 })
        this.text = markup("<div>some content</div>")
        this.state = useState({ open: true });
    }

    increment() {
        this.clicks.value++;
        if (this.props.onCardClick) {
            this.props.onCardClick();
        }
    }

    toggle() {
        this.state.open = !this.state.open;
    }

    reset() {
        if (this.props.onCardClick) {
            this.props.onCardClick(this.clicks.value);
        }
        this.clicks.value = 0;
        
    }
}
