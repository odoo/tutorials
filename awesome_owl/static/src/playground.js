import { Component, markup, useState } from "@odoo/owl";
import { Card } from "./card/card"
import { Counter } from "./counter/counter"
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Card, Counter, TodoList };

    setup() {
        this.state = useState({value: 2});
        this.onChange = this.onChange.bind(this);
    }

    onChange() {
        this.state.value++;
    }
}
