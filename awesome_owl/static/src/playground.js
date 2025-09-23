import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.state = useState({ sum: 2 });
        this.incrementSum = this.incrementSum.bind(this);
    }

    fst_value = markup("<strong>fst</strong>");
    snd_value = "<em>snd</em>";

    incrementSum() {
        this.state.sum++;
    }

}
