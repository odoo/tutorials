import { Component, markup, onMounted, onWillStart, useState } from "@odoo/owl";
import { Counter } from "./components/counter/counter";
import { Card } from "./components/card/card";
import { TodoList } from "./components/todo/todoList/todoList";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.sum = useState({ value: 2 });
        this.todos = useState([
            { id: 1, description: "buy milk", isCompleted: false },
            { id: 2, description: "Improve Skills", isCompleted: false },
            { id: 3, description: "Practice", isCompleted: false },
        ]);
    }

    increaseCount() {
        this.sum.value++;
    }

    html = markup("<h1>HELLO I AM YASH</h1>");
}
