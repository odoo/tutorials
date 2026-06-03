import {Component, markup, useState} from "@odoo/owl";
import {Counter} from "./counter/counter";
import {Card} from "./card/card";
import {TodoList} from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = {Counter, Card, TodoList};

    setup() {
        this.htmlContent1 = markup("Some <strong>bold</strong> text content.");
        this.htmlContent2 = markup("<span class='text-primary'>Reusable</span> components are great!");

        this.counter = useState({
            value1: 0,
            value2: 0,
        });
    }

    resetCounters() {
        this.counter.value1 = 0;
        this.counter.value2 = 0;
    }
}
