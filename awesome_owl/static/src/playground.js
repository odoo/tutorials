/** @odoo-module **/
import { Component, markup, useState, useRef, onMounted } from "@odoo/owl";
import { Card } from "./card/card";
import { Counter } from "./counter/counter";
import { TodoList } from "./Todo/TodoList";

export class Playground extends Component {
    static template = "awesome_owl.playground";;
    text1 = "<div class='text-primary'> some content</div>";
    text2 = markup("<div class='text-primary'> some content</div>");
    setup() { this.state = useState({ sum: 2 }); }

    incrementSum(CounterValue) {
        this.state.sum++;

    }
    static components = { Counter, Card, TodoList }
}
