import { Component, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todolist"


export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = { Counter, Card, TodoList };

    setup() {
        this.state = useState({ value : 2 });
    }

    incrementSum() {
        this.state.value++;
    }
}
