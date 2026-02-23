import { Component, useState } from "@odoo/owl";
import { Counter } from "./components/counter/counter";
import { Card } from "./components/card/card";
import { TodoList } from "./components/todoo/todo_list/todo_list";
export class Playground extends Component {
    static template = "awesome_owl.Playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.sum = useState({ value: 0 });
    }
    incrementSum() {
        this.sum.value++;
    }
}
