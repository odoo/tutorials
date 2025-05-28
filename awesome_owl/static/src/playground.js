/** @odoo-module **/

import { Component, useState, markup} from "@odoo/owl";
import { Counter } from "./counter/counter"
import { Card } from "./card/card";
import { TodoList } from "./todo_list/todo_list";


export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList}
    html_stuff = markup("<h2>hello</h2>")

    setup() {
        this.incrementSum = this.incrementSum.bind(this)
        this.state = useState({ sum:0 });
    }

    incrementSum() {
        this.state.sum++;
    }
}
