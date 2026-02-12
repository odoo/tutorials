/** @odoo-module **/
import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.Playground";
    static props = {};
    static components = { Counter, Card, TodoList };
    setup() {
        this.safeHtml = markup("<b>Bold HTML</b> with <i>markup()</i>");
        this.unsafeHtml = "<b>This will NOT be bold</b>";
        this.state = useState({ sum: 0 });
        this.c1 = 0;
        this.c2 = 0;
    }

    onCounter1Change(val) {
        this.c1 = val;
        this.state.sum = this.c1 + this.c2;
    }

    onCounter2Change(val) {
        this.c2 = val;
        this.state.sum = this.c1 + this.c2;
    }

}
//Playground.template = "awesome_owl.Playground";
