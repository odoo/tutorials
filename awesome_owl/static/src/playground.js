/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo_item/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.sum = useState({ total:2 });
        this.safeHTML = "<div class='text-primary'>some content</div>";
        this.normalString = markup("<div class='text-primary'>some content</div>");
    }

    incrementSum() {
        this.sum.total++;
    }
}
