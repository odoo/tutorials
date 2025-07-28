/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.Counter";
    static props = {
        // RICEVO: callback dal parent (opzionale)
        onIncrement: { type: Function, optional: true }
    };

    setup() {
        this.state = useState({ value: 0 });
    }

    increment() {
        this.state.value++;
        
        // INVIO: notifico il parent del nuovo valore
        if (this.props.onIncrement) {
            this.props.onIncrement(this.state.value);
        }
    }
}
