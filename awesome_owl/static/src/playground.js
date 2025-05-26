/** @odoo-module **/

import { Component, markup, useState} from "@odoo/owl";

import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";


export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = { Counter, Card, TodoList}

    title = "<div style='color:blue'> Title </div>"
    content = "<div style='color:blue'> content </div>"
    
    safeTitle = markup("<div style='color:blue'> Title </div>")
    safeContent = markup("<div style='color:blue'> content </div>")


    setup() {
        this.state = useState({ 
            counter1: 0, 
            counter2: 0,
        });
    }

    get sumCounters() {
        return this.state.counter1 + this.state.counter2
    }

    increment_counters(counterNumber) {
        counterNumber == 1 ? this.state.counter1++ : this.state.counter2++ 
    }
}
