/** @odoo-module **/
import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.state = useState({
            sum: 0
        });

        this.textContent = "OK <strong> NOW </strong>";
        this.htmlContent = markup("NOW <strong> OK </strong>");


        this.updateSum = (value) => {
            this.state.sum = this.state.sum + value
        }
    }
}
