/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import {Counter} from "./counter/counter";
import {Card} from "./card/card";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    setup() {
        this.sum = useState({ value: 0 });
    }

    onIncrement() {
        this.sum.value++;
    }
    static components = { Counter, Card, TodoList };
}
