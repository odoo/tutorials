/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Counter } from "./counter";
import { Card } from "./card/card";
import { TodoList } from "./components/todoList";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList};

    setup() {
        this.sum = useState({value:2 })
        this.addCount = this.addCount.bind(this);
    }

    increment(){
        this.state.value++;
    }

    addCount(count)
    {
        this.sum.value = this.sum.value + count;
    }
}
