import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        const productDescriptionFromDB = "<p>This is a <strong>great</strong> product!</p>";
        this.description = markup(productDescriptionFromDB);
        this.sum = useState({ value: 0 });

        this.someExpression = () => {
            return true;
        }
    }

    incrementSum() {
        this.sum.value++;
    }
}
