/** @odoo-module **/

const { Component, useState } = owl;
import { Card } from "./card/card";
import { Counter } from "./counter/counter";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = { Counter, Card, TodoList };

    setup() {
        this.sum = useState({ value: 2 });
        this.str1 = "some content for str1";
        this.str2 = "some content for str2";
        // I want to have an example of markup
        // this.str2 = markup("<div class='text-primary'>some content</div>");
    }

    incrementSum() {
        this.sum.value++;
    }
}
