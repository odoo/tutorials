import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "../counter/counter";
import { Card } from "../card/cards";
import { TodoList } from "../todo/TodoList";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList};
    static props = {};


    setup() {
        this.state = useState({ sum: 2 });
        this.normalText = "<b>Normal String</b>";
        this.htmlText = markup("<b>Bold Text</b>");
    }
    incrementSum() {
        this.state.sum += 1;
    }
}
