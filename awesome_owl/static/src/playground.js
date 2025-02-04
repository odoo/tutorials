/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Card } from "./Card/card";
import { Counter } from "./Counter/counter"
import { TodoList } from "./TodoList/todolist";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    setup(){
        this.state = useState({ sum: 0 });
        this.findSum = this.findSum.bind(this);
    }

    findSum(){
        this.state.sum++;
    }

    title1 = ("Card 1")
    content1 = ("<div class='text-primary'>content of card 1</div>")
    title2 = markup("<div>Card 2</div>")
    content2 = markup("<div class='text-primary' >content of card 2</div>")

    static components = { Card, Counter, TodoList };
}
