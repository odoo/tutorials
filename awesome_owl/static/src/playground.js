import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = {Counter, Card, TodoList}

    setup() {
        this.state = useState ({
            sum:2
        });

        this.textContent = "Koradiya <strong> Patel </strong>";
        this.htmlContent = markup("Koradiya <strong> Patel </strong>");
    

    this.updateSum = (value) => {
        this.state.sum = this.state.sum + value
        }
    }
}

