import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo_list/TodoList";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };
    static props = {};
    setup() {
        this.sum = useState({value : 2})
        this.incrementSum = () => {
            this.sum.value++;
        }
    }
}
