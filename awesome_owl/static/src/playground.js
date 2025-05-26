/** @odoo-module **/

import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { Todo_list } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = {Counter, Card, Todo_list};
    static props = {};
    
    raw_title = "<u>Title</u>"
    raw_content = "<u>Content</u>"
    content= markup("<u>Content</u>")
    title = markup("<u>Title</u>")

    setup() {
        this.sum = useState({ value: 2 });
    }

    incrementSum() {
        this.sum.value++;
    }
}
