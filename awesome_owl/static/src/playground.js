/** @odoo-module **/

import { Component , markup , useState } from "@odoo/owl";
import { Counter } from "./Counter/counter";
import { Card } from "./Card/card";
import { TodoList } from "./TodoList/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    static props = {};

    // Register Counter so it can be used in the template
    static components = { Counter , Card , TodoList };

    setup() {
        this.content_1 = markup("<div style='color:red;'>This is safe HTML</div>");
        this.content_2 = "<div style='color:blue;'>This will be escaped</div>";
        this.state = useState({ sum: 0 });
    }

    incrementSum() {
        this.state.sum++;
    }
}