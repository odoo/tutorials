/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo_list/todo_list";
export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.html = markup("<div>some content</div>")
        this.total=useState({value:0})
    }
    sum() {
        this.total.value++;
    }
    sub(){
        this.total.value--;
    }
}
