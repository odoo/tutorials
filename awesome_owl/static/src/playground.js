// playground.js
import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./ToDo/todolist";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = {Counter, Card, TodoList};

    setup() {
        this.sum = useState({ value: 2 }),
        this.content1 = "<div class='text-primary'>content 1</div>";
        this.content2 = markup("<div class='text-primary'>content 2</div>");
    }

    incrementSum() {
        this.sum.value++;
    }
}
