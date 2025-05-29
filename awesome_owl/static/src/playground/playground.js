/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Counter } from "../components/counter/counter";
import { TodoList } from "../components/todo_list/todo_list";
import { Card } from "../components/card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground.view";
    static components = { Counter, TodoList, Card };

    setup() {
        this.state = useState({
            count1: 0,
            count2: 0
        });
    }

    updateCount = (counterName, newCount) => {
        if (counterName in this.state) {
            this.state[counterName] = newCount;
        }
    }

    get sum() {
        return this.state.count1 + this.state.count2;
    }
}
