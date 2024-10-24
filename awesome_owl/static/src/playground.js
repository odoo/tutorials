/** @odoo-module **/

import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { markup, Component, useState } from "@odoo/owl";


export class Playground extends Component {
    static template = "awesome_owl.playground";


    setup() {
        this.incrementSum = this.incrementSum.bind(this);
        this.state = useState({ sum: 2 });
    }

    incrementSum() {
        this.state.sum++;
    }

    static components = { Counter, Card };
}
