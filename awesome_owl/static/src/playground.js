/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = { Counter, Card, TodoList }

    // html = markup("some <b>cool</b> content")
    sum = useState({ value: 0 })

    incrementSum() {
        this.sum.value++;
    }
}
