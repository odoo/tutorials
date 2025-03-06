/** @odoo-module **/

const { Component, useState } = owl;

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        title: String,
        slots: { type: Object, optional: true }
    }

    setup = () => {
        this.state = useState({value: 'open'});
    }

    toggleState = () => {
        this.state.value = this.state.value === 'open' ? 'closed' : 'open';
    }
}
