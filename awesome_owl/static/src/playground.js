import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static props = {};
    static components = {
        Counter,
        Card,
        TodoList,
    };
    setup() {
        this.html = markup("<div>this is html content</div>");
        this.state = useState({
            sum: 0,
        });
    }

    sum({ value, operator }) {
        if (operator === -1) {
            this.state.sum--;
        } else {
            this.state.sum++;
        }
    }
}
