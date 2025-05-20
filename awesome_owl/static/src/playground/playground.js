/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Counter } from "../components/counter/counter";
import { TodoList } from "../components/todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground.view";
    static components = { Counter, TodoList };

    setup() {
        this.state = useState({
            count1: 0,
            count2: 0,
        });
    }

    updateCount1(newCount) {
        this.state.count1 = newCount;
    }

    updateCount2(newCount) {
        this.state.count2 = newCount;
    }

    get sum() {
        return this.state.count1 + this.state.count2;
    }
}
