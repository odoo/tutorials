import { Component, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { markup } from "@odoo/owl";
import { TodoList } from "./todo-list/todo-list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card ,TodoList};

    setup() {
        this.html = markup("<b>Hello World!</b>");
        this.state = useState({ 
            count1: 0, 
            count2: 0 
        });
    }

    updateCount1(val) {
        this.state.count1 = val;
    }

    updateCount2(val) {
        this.state.count2 = val;
    }
}
