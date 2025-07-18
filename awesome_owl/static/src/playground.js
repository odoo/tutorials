/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./components/counter/counter"
import { Card } from "./components/card/card"
import { TodoList } from "./components/todo/todo_list/todo-list";

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
