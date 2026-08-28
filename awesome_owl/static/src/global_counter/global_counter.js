import { Component, useState } from "@odoo/owl";
import { Counter } from "../counter/counter";

export class GlobalCounter extends Component {
    static template = "awesome_owl.global_counter";

    static components = {
        Counter
    }

    static props = {
        buttons: Number
    }

    setup() {
        this.buttons = []
        for (let i = 0; i < this.props.buttons; i++) {
            this.buttons.push(i)
        }

        this.state = useState({ value: 2 });
        this.incrementSum = this.incrementSum.bind(this)
    }

    incrementSum() {
        this.state.value++;
    }
}
