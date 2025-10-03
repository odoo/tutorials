/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todolist";


export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };
    sum = useState({ value: 2 });
    state = useState({ a: markup("<div class='text-primary'>content of card</div>") })
    incrementSum() {
        this.sum.value++;
    }
}
