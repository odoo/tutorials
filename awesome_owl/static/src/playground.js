import { Component } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.Playground"; //
    static components = { Counter, Card }; //

    setup() {
        this.cards = [
            { title: "Card 1", content: "This is the content for Card 1." },
            { title: "Card 2", content: "This is the content for Card 2." },
            { title: "Card 3", content: "This is the content for Card 3." }
        ];
    }
}
