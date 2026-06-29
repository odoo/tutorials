import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.html="<b>keyur maniar from gujrat</b>"
        this.mark=markup("<b>keyur maniar from gujrat</b>");

        this.state = useState({
            sum: 0
        });
    }

    incrementsum() {
        this.state.sum++;
    }
}