import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";


export class Playground extends Component {
    static template = "awesome_owl.playground";
    static props = {};
    static components = { Counter, Card, TodoList };

    setup() {
        this.state = useState({
            content: markup('<h1>Welcome to dashboard</h1>'),
            sum: 0, 
        });

    }

    totalSum(newVal,Checker){
        if(Checker)
            this.state.sum++;
        else
            this.state.sum--;
    }
}
