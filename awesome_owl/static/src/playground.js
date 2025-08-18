import { Component, markup, useState } from "@odoo/owl";

import { Counter } from "./counter";
import { Card } from "./card";
import { TodoList } from "./todoList";


export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Card, Counter, TodoList };

    setup(){
        this.state = useState({sum: 2});
        this.incrementSum = this.incrementSum.bind(this);
    }

    incrementSum() {
        this.state.sum++;
    }
}
