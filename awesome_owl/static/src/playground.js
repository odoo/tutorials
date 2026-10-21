import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter";
import { Card } from "./card";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup(){
        this.html = markup("<div class='text-primary'>This html is rendered in blue.</div>");
        this.plainText = "<div class='text-primary'>This is plain text,not HTML.</div>";

        this.state = useState({ sum: 2});
    }

    incrementSum(){
        this.state.sum++;
    }
}
