import { markup, Component, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todolist";


export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.state = useState({
            content: markup('<h1>Welcome to your Counter!</h1>'),
            sum: 0
        });
    }

    calculateSum(newValue) {
        if (newValue > 0) {
            this.state.sum++;
        }
        if (newValue < 0) {
            this.state.sum--;
        }
    }

    reset() {
        this.state.sum = 0
    }
}
