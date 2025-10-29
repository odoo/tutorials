import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "@awesome_owl/counter/counter";
import { Card } from "@awesome_owl/card/card";
import { TodoList } from "@awesome_owl/todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };
    static props = {};

    setup() {
        this.state = useState({
            sum: 2,
        });

        this.counterValues = [1, 1];

        this.str1 = markup("<div class='text-primary'>some content</div>");
        this.str2 = "<b>some content</b>";
    }

    updateCounterValue(index, newValue) {
        this.counterValues[index] = newValue;
        this.state.sum = this.counterValues.reduce((a, b) => a + b, 0);
    }

    onChange1 = (val) => this.updateCounterValue(0, val);
    onChange2 = (val) => this.updateCounterValue(1, val);
}
