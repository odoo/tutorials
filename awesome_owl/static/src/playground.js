import {Component, useState} from "@odoo/owl";
import { Card } from "./card/card";
import { Counter } from "./counter/counter";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.sum = useState({ value: 0 });
    }

    incrementSum() {
        this.sum.value++
    }
}
