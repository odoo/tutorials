/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo_list/todo_list";
import { TodoItem } from "./todo_list/todo_item";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList, TodoItem };

    // sum = useState({ value: 0 });

    // sumOfCounters = () => {
    //     this.sum.value++;
    // }

    // toggle = (ev) => {
    //     console.log(ev)
    // }
}
