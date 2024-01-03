/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };
    state = useState({ sum: 0 });

    get cardContent(){
        return markup('<strong>some text 1</strong>');
    }

    incrementSum(value) {
        this.state.sum += value;
    }
}