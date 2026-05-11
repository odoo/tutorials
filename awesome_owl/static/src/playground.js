import { Component, xml, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import {TodoList} from "./Todo/todolist"

export class Playground extends Component {
    static template = "awesome_owl.playground"
    static components = { Counter, Card, TodoList }

    setup() {
        this.val1 = "<div>Hello I am Code</div>"
        this.val2 = markup("<div>Hello I am Code</div>")
        this.sum = useState({ value: 2 })
    }

    incrementOfSum() {
        this.sum.value++
    }
}
