/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todolist/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    setup() {
        this.state = useState({ sum: 2 });
        this.html = "<div class='text-primary'>Some Content</div>";
        this.Markuphtml = markup("<div class='text-primary'>Some Content</div>");
    }

    incrementSum(){
        this.state.sum++;
    }

    static components = { Counter , Card, TodoList}

}
