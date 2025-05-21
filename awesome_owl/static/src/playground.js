/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Counter } from "@awesome_owl/counter/counter";
import { TodoList } from "@awesome_owl/todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, TodoList };

    setup() {
        this.state = useState({
            sum: 0,
            todos: [],
        });
    }

    incrementSum() {
        this.state.sum++;
    }
}
