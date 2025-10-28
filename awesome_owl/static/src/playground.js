/** @odoo-module **/

import {Component, useState} from "@odoo/owl";
import {Counter} from "./counter/counter";
import {Card} from "./card/card";
import {TodoList} from "./TodoList/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static props = {};
    static components = {Counter, Card, TodoList}

    setup() {
        this.state = useState({
            sum: 2,
        })
    }

    incrementSum() {
        this.state.sum++;
        console.log(this.state.sum)
    }
}
