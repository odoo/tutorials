import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";

    static props = {
        title: String,
        slots: {
            type: Object,
            optional: true,
        },
        isOpen: Boolean,
    }

    state = useState({ isOpen: this.props.isOpen });

    onToggleOpen(){
        this.state.isOpen = !this.state.isOpen
        console.log(this.state.isOpen)
    }
}
