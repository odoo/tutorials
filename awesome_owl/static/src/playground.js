/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Counter } from './counter/counter.js'
import { Card } from './card/card.js'
import { TodoList } from './todo/todo_list.js'

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList }

    setup() {
        this.sum = useState({ value: 0 });
    }

    handleCounterChange(component, oldValue) {
        this.sum.value += component.counter.value - oldValue;
    }
}
