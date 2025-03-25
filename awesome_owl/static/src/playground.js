/** @odoo-module **/

import { Component, markup, useState} from "@odoo/owl";
import { Counter } from "./Counter/counter";
import { Card } from "./Card/card";
import { TodoList } from "./Todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };
    static props = {};

    setup(){
        this.unsafehtml= "<div class='text-primary'>some content</div>";
        this.safehtml = markup("<div class='text-primary'>some content</div>");

        this.state = useState({ sum: 0 });
        this.incrementSum = this.incrementSum.bind(this);  //alt:we ccan also use arrow function, if we do not want to use bind()
    }

    incrementSum() {
        this.state.sum++;
    }
}
