import { Component, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card"
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, TodoList, Card };

    setup(){
       this.state =useState({ sum: 2 });
       this.incrementSum = this.incrementSum.bind(this);
    }

    incrementSum() {
        this.state.sum++;
    }
}
