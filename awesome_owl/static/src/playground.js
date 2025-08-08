/** @odoo-module **/
import { markup, useState, Component } from "@odoo/owl";
import { Counter } from "./Counter/counter";
import { Card } from "./Card/card";
import { TodoList } from "./TodoList/todo_list";

export class Playground extends Component {
    static components = { Counter, Card, TodoList };
    static template = "awesome_owl.playground";

    setup() {
        this.state = useState({ sum: 2 });
    }

    incrementSum() {
        this.state.sum++;
    }

    // content_1 = "<div class='text-primary'> content of card 1</div>";
    // content_2 = markup("<div class='text-primary'> content of card 2</div>");

}
