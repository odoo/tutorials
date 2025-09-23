/** @odoo-module **/

import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card };

    setup() {
        this.state = useState({ sum: 2 });
        this.incrementSum = this.incrementSum.bind(this);  // Bind the method to its instance
    }

    incrementSum(){
        this.state.sum++; 
    }

    cards = [
        { title: "Card 1", content: markup("<div>some content</div>") },
        { title: "Card 2", content: "This is the second card." },
        { title: "Card 3", content: "Another card example." },
    ];
}
