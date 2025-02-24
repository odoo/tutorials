import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.Card"; // Link to the Card template
    static props = {
        title: String,
        slots: {
            type: Object,
            shape: {
                default: true
            }
        }
    };

    setup() {
        this.validateProps();
        this.state = useState({ isExpanded: false });
    }

    toggleExpansion() {
        this.state.isExpanded = !this.state.isExpanded
    }
    validateProps() {
        if (typeof this.props.title !== 'string') {
            console.error('Prop `title` should be a string!');
        }
    }
}
