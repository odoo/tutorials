import { Component, useState, markup } from "@odoo/owl";

import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card };

    setup() {
        this.state = useState({ sum: 2 });
    }

    incrementSum() {
        this.state.sum++;
    }
}