import { Component, mount, useState } from "@odoo/owl";
import { Card } from "./card/card"
import { Counter } from "./counter/counter";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.Playground";
    static components = { Card, Counter, TodoList };

    setup() {
        this.state = useState({
            sum: 0,
            rawHtml: "<b>This will NOT be bold</b>",
            safeHtml: "<b>This WILL be bold</b>",
        });
    }

    incrementSum(value) {
        this.state.sum += value;
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const app = document.getElementById("playground");
    if (app) {
        mount(Playground, { app });
    }
});
