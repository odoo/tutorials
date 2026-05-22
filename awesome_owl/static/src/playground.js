import { Component, useState } from "@odoo/owl";
import { markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.state = useState({
            sum: 0,
        });
        this.htmlContent = markup("<div class='text-primary'>heloo odoo</div>");
        this.normalContent = "<div class='text-danger'>hel0o world</div>";
    }
    
    incrementSum(xyz) {
        this.state.sum += xyz;
    }
}
