import { Component, useState } from "@odoo/owl";
import { Card } from "@awesome_owl/card/card";
import { Counter } from "@awesome_owl/counter/counter";
import { TodoList } from "@awesome_owl/todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static props = {
        onChange: { type: Function, optional: true },
    };

    setup() {
        this.sum = useState({ value: 2 });
        this.str1 = "content of card 1"
        this.str2 = "content of card 2"
    }

    incrementSum() {
        this.sum.value++;
    }

    static components = { Counter, Card, TodoList };
}
