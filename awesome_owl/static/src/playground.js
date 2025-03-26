/** @odoo-module **/

import { Component,useState, markup } from "@odoo/owl";
import {Counter} from "./components/counter/counter";
import  {Card}  from "./components/card/card";
import TodoList from "./components/todolist/todolist";

export class Playground extends Component {
    static template = "awesome_owl.Playground";
    static components = { Counter, Card, TodoList };
    static props = {};
    setup() {
        this.plainContent = "<div class='text-primary'>some content</div>";
        this.htmlContent = markup("<div class='text-primary'>some content</div>");
        this.state = useState({ sum: 2 });
        this.incrementSum = this.incrementSum.bind(this);
    }
    incrementSum() {
        this.state.sum++;
    }
}
