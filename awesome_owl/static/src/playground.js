/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todos/todoList";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup(){
        this.sum = useState({ value: 2 });
        this.content = markup('<h1>Hello</h1>');
    }

    incrementSum(){
        this.sum.value++;
    }
    
}
