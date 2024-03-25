/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoList } from "./todo_list/todo_list";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { TodoList, Counter, Card };

    setup() {
        this.state = useState({ sum: 0 });
    }

    incrementSum() {
        this.state.sum++;
    }
}
