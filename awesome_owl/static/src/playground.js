import { Component, useState, markup } from "@odoo/owl";

import { Counter } from "./components/counter/counter";
import { Card } from "./components/card/card"

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card };

    counter = useState({ value: 0 });

    card1Content = "<div class='text-primary'>some content</div>"
    card2Content = markup("<div class='text-primary'>some content</div>")

    increment() {
        this.counter.value += 1
    }
}
