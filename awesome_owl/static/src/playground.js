/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Counter } from "@awesome_owl/counter/counter";
import { Card } from "@awesome_owl/card/card";
import { TodoList } from "@awesome_owl/todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static props = [];
    static components = { Counter, Card, TodoList };

    setup() {
        this.sum = useState({ value: 0 });
    }
    incrementSum() {
        this.sum.value++;
    }
}
