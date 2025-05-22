/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "../counter/counter";
import { Card } from "../card/card";
import { TodoList } from "../todolist/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = {Counter, Card, TodoList}

    setup(){
        this.state = useState({
            counter1: 1,
            counter2: 1,
            sum:2,
        });
    }

    calculateSum=(counterName, value)=>{
        this.state[counterName]=value
        this.state.sum = this.state.counter1 + this.state.counter2;
    }

    cards = [
        {
            id:1,
            title: "Card 1",
            content: "Just a simple text (escaped by default)",
        },
        {
            id:2,
            title: "Card 2",
            content: markup("<strong>Bold HTML content</strong>"),
        },
        {
            id:3,
            title: "Card 3",
            content: markup("<div style='color: red;'>Red colored HTML</div>"),
        },
    ];
}
