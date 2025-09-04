/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Counter } from "@awesome_owl/components/counter/counter";
import { Card } from "@awesome_owl/components/card/card";
import { TodoList } from "@awesome_owl/components/todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.state = useState({ sum: 0 });
    }

    incrementSum() {
        this.state.sum++;
    }
}
