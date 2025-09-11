/** @odoo-module alias=@awesome_owl/ default=false**/

import { TodoList } from "@awesome_owl/todo_list/TodoList";
import { Component, useState } from "@odoo/owl";
import { Card } from "@awesome_owl/card/Card";
import { Counter } from "@awesome_owl/counter/Counter";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.sum = useState({ value: 0 });
    }

    incrementSum() {
        this.sum.value++;
    }

    decrementSum() {
        this.sum.value--;
    }
}
