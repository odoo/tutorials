/** @odoo-module **/

import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "../Counter/counter";
import { Card } from "../Card/card";
import {TodoList} from "../Todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card , TodoList};

    setup() {
        this.state = useState({
            counter1: 1,
            counter2: 1,
            sum: 2
        });
      
    }
     incrementSum =(counterName, value)=> {
        this.state[counterName] = value;
        this.state.sum = this.state.counter1 + this.state.counter2;
    }
}
