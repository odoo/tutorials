import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter";
import { Card } from "./card";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static components = {
        Counter,
        Card,
        TodoList,
    };
    static template = "awesome_owl.Playground";

    setup() {
        this.state = useState({ sum: 0 });
    }

    incrementSum() {
        this.state.sum++;
    }
}
