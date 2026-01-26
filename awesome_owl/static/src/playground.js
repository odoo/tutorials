import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";


export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.htmlContent1 = "<div class='text-danger'>This is second card text - not marked up</div>";
        this.htmlContent2 = markup("<div class='text-primary'>This is third card text - marked up</div>");
        this.state = useState({
            sum: 2,
        });
    };

    incrementSum() {
        this.state.sum++;
    };
}
