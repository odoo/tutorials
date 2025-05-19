/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";
import { TodoItem } from "./todo/todo_item";

export class Playground extends Component {
    static template = "awesome_owl.Playground";

    static components = { Counter, Card, TodoList, TodoItem };

    static props = {
    };

    setup() {
        this.state = useState({ value: 0 });
    }

    incrementSum() {
        this.state.value++;
    }
}
