import { Component, useState } from "@odoo/owl";

import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.sum = useState({ value: 2 }); 
        this.incrementSum = () =>{
            this.sum.value++; // Increase sum whenever a counter increments
        }
    }

}
