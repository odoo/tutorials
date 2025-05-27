/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Card } from "./card/card";
import { Counter } from "./counter/counter";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.title = "[Odoo] New version here!!!";
        this.sum = useState({value: 0});
    }

    incrementSum() {
        this.sum.value++;
    }
}
