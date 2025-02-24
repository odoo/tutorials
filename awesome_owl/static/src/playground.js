/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todolist/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.state =  useState({ sum: 2 });
        this.mark = markup("<div>some content</div>");
        this.nomark = "<div>some content</div>";
    }

    incrementSum(value) {
        this.state.sum += value;
    }
}
