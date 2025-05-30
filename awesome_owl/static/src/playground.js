/** @odoo-module **/

import {Component, useState} from "@odoo/owl";
import {Counter} from "./counter/counter";
import {Card} from "./card/card";
import {TodoList} from "./todo/todo_list";


export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = {Counter, Card, TodoList};

    state = useState({globalCount: 0})

    setup() {
        this.incrementBind = this.increment.bind(this);
    }

    increment() {
        this.state.globalCount++;
    }
}
