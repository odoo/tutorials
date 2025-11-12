/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./misc/counter";
import { Card } from "./misc/card";
import { TodoList } from "./todo/todo_list"

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList }
    static props = {}
    setup(){
        this.message_1 = "<div class='text-primary'>Content 1</div>"
        this.message_2 = markup("<div class='text-primary'>Content 2</div>")
        this.counter_sum = useState({ value: 0 })
    }
    onCounterIncrement(){
        this.counter_sum.value++;
    }
}
