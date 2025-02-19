/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./components/card"
import { TodoList } from "./components/Todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList }
    text = markup("<div class='text-primary'>markup text</div>")

    setup(){
        this.state = useState({ sum: 2})
    }

    incrementSum(){
        this.state.sum++;
    }
}
