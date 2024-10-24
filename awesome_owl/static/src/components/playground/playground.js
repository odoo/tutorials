/** @odoo-module **/

import {Component, useState} from "@odoo/owl";

import {Counter} from "../counter/counter";
import {Card} from "../card/card"
import {TodoList} from "../todo_list/todo_list"

export class Playground extends Component {
    static components = {Counter, Card, TodoList};

    static template = "awesome_owl.playground";

    setup() {
        this.state = useState({sum: 0})
        this.incrementSum = this.incrementSum.bind(this);
    }

    incrementSum() {
        this.state.sum++;
    }
}
