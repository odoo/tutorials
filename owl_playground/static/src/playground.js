/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { TodoList } from "./todo/todo";
import { Card } from "./card/card";

export class Playground extends Component {
    setup() {
        this.state = useState({count: 0})
        this.todo =  useState({

            list: [
            // commenting it and making it dynamic
                // { id: 300, description: "check PR", done: false },
                // { id: 400, description: "review task", done: true},
                // { id: 500, description: "Team Meeting", done: true},
            ],
            count: 0,
        });
        if(localStorage.getItem('todo_list') && localStorage.getItem('todo_list')) {
            this.todo.list = JSON.parse(localStorage.getItem('todo_list'));
            this.todo.count = JSON.parse(localStorage.getItem('todo_count'));
        }
        // this.increment = this.increment.bind(this);
    }

    increment() {
        console.log('hgi');
        debugger;
        this.state.count++;
    }
}

Playground.components = { Counter, TodoList, Card }
Playground.template = "owl_playground.playground";
