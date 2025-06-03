import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./components/counter/counter";
import { Card } from "./components/card/card";
import { TodoItem } from "./components/todoitem/todoitem";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    setup() {
        this.cards = [
            {
                title: "Card 1 Title",
                content: markup(
                    "<div><strong>This is bold content for Card 1!</strong></div>"
                ),
            },
            {
                title: "Card 2 Title",
                content: markup(
                    "<div><em>This is italic content for Card 2!</em></div>"
                ),
            },
        ];

        this.state = useState({ value: 0 });
        this.sum = this.sum.bind(this);
    }
    sum() {
        this.state.value++;
    }
    static components = { Counter, Card };
}
