/** @odoo-module **/
import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template   = "awesome_owl.Playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.state      = useState({ sum: 0 });
        this.safeHtml   = markup("<div class='text-primary'>some content</div>");
        this.unsafeHtml = "<div class='text-primary'>some content</div>";
    }

    updateSum(value) {
        this.state.sum += value;
    }
}
