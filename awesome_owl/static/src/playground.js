import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";


export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };
    static props = {};

    title = markup("<div class='text-primary'> title 1 </div>")
    content = markup("<div class='text-secondary'> some content </div>")
    setup() {
        this.state = useState({ counterSum: 2 });
    }
    sumIncrement() {
        this.state.counterSum++
    }
}
