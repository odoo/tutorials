import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";
import { TodoItem } from "./todo/todo_item";


const exampleHtml = "<div class='text-primary'>some content</div>";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = { Counter, Card, TodoItem, TodoList };
    // static components = {Counter, Card};

    html = exampleHtml;
    markupHtml = markup(exampleHtml);

    setup() {
        this.state = useState({ sum: 0 });
    }

    onChange(){
        this.state.sum ++;
    }

}
