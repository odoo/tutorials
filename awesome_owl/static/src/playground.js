import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "awesome_owl/components/counter/counter";
import { Card } from "awesome_owl/components/card/card";
import { TodoList } from "awesome_owl/components/todo/todo_list/todo-list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = {Counter, Card, TodoList};
    static props = {};
    setup() {
        this.state = useState({
            sum: 0
        });
        this.adjustSum = (delta) => {
            this.state.sum += delta;
        };
        this.htmlContent = markup("<div class='text_primary' style='color: DodgerBlue;'>This is bold HTML content</div>");
        this.plainContent = "<div class='text_primary'>This will be escaped</div>";
    }
}
