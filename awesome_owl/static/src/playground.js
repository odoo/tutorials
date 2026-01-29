import { Component, markup, useState } from "@odoo/owl";
import { Counter} from "./Counter/Counter";
import { Card } from "./Card/Card";
import { TodoList } from "./Todo/TodoList";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = {Counter, Card, TodoList}

    setup() {
        this.state = useState({ count: 0, sum: 0});
    }

    increment() {
        this.state.count++;
    }

    incrementSum(delta){
        this.state.sum += delta;
    }

    value1=markup`<div class='text-info'> This is a first content! </div>`;
}
