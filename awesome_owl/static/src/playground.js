import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./components/counter/counter";
import { Card } from "./components/card/card";
import { TodoList } from "./components/todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = { Counter, Card, TodoList };

    value1 = "<b>Some HTML content</b>";
    value2 = markup("<b>Some other HTML content</b>");

    setup () {
        this.state = useState({sum: 0});
    }

    onCounterChange () {
        this.state.sum += 1;
    }
}
