import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.Playground";
    static components = { Counter, Card, TodoList};
    setup() {
        this.sum = useState({count:2});
        this.cards = useState([
            { title: "Card 1", content: "This is a <strong>normal string</strong>" },  // Will be escaped
            { title: "Card 2", content: markup("<div style='color: red;'>This is safe HTML</div>") }, // Will render as HTML
            { title: "Card 3", content: "A simple text message" } // Normal string, escaped
        ]);
    }
    incrementSum(){
        this.sum.count = this.sum.count + 1; // Increment sum by 1 each time
    };
}