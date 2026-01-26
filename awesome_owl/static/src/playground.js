import { Component, useState } from "@odoo/owl";
import { Card } from "./card/card";
import { Counter } from "./counter/counter";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Card, Counter };

    setup() {
        this.state = useState({
            cards: [
                { id: 1, title: "Card 1", folded: false, count: 0 },
                { id: 2, title: "Card 2", folded: false, count: 0 },
                { id: 3, title: "Card 3", folded: false, count: 0 },
            ]
        });
    }

    get totalCount() {
        return this.state.cards.reduce((acc, card) => acc + card.count, 0);
    }

    increment(card) {
        card.count++;
    }

    toggleFold(id) {
        const card = this.state.cards.find((card) => card.id === id);
        if (card) {
            card.folded = !card.folded;
        }
    }

}
