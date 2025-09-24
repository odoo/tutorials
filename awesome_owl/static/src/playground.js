/** @odoo-module **/

import { Component, useState, markup } from "@odoo/owl";
import { TodoList } from "./todo/todo_list";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.state = useState({ sum: 2 });
    }

    incrementSum(){
        this.state.sum++; 
    }

    cards = [
        { title: "Card 1"},
        { title: "Card 2"},
        { title: "Card 3"},
    ];
}
