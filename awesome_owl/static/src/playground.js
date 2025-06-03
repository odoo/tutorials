/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo_list/todo_list";       

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList};

    setup() {
        this.state = useState({sum: 0})
    }

    incrementSum() {
        console.log("Incrementing sum function called!");
        console.log("Current sum:", this.state.sum);
        this.state.sum += 1;
        console.log("New sum:", this.state.sum);
    }
}