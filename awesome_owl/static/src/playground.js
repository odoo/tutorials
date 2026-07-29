import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card }

    content = markup("<div> some texte 2</div>")

    setup() {
        this.sum = useState({ value: 0 });
    }

    incrementSum() {
        this.sum.value++
    }
}