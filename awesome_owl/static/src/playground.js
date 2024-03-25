/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    html = markup(`
        <div>
            <a href="#" t-on-click="showCounter">Show Counter</a>
        </div>
    `);

    setup() {
        this.state = useState({ value: 0 });
    }

    incrementSum() {
        this.state.value++;
    }
}
