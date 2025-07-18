/** @odoo-module **/

import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./components/counter/counter";
import { Card } from "./components/card/card";
import { TodoList } from "./components/todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter,Card, TodoList };
    

    setup(){
        this.state = useState({ sum : 0 });
        this.html = markup("<div>some content</div>");
    }

    incrementSum(){
        this.state.sum++;
    }
}
