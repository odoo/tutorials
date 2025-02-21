/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./Todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.Playground";

    static components = { Counter, Card, TodoList };

    setup(){
        this.state = useState({ sum: 0 });
    }
    incrementSum(){
        this.state.sum += 1;
    }

    static props = {};
}
