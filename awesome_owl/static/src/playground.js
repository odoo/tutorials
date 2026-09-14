import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.html = "<b>Hello I'm Abhishek</b>"
        this.mark = markup("<b> Hello I'm Abhishek</b>")

        this.state = useState({
            sum: 0
        });
    }

    incrementSum() {
        this.state.sum++;
    }

}
