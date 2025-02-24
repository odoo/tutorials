// import { Component, useState } from "@odoo/owl";
import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todoList/todoList";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };
    
    value1 = "<div class='text-primary'>some content</div>";
    value2 = markup("<div class='text-primary'>some content</div>");

    setup() {
        this.sum = useState({value: 2});
    }
    onchange() {
        this.sum.value++;
    }
}
