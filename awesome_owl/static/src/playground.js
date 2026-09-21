import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.counters = useState({ sum: 2 });
        this.contents = useState({ content1: "<p>Content 1</p>", content2: markup("<p>Content 2</p>") });

        this.incrementSum = this.incrementSum.bind(this);
    }

    incrementSum() {
        this.counters.sum++;
    }
}
