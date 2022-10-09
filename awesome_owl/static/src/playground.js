import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.str1 = "<div class='text-primary'>some content</div>";
        this.str2 = markup("<div class='text-primary'>some content</div>");
        this.counters = useState([
            { value: 1},
            { value: 10 },
            { value: 100 }
        ]);
    }

    get sum() {
        return this.counters[0].value + this.counters[1].value + this.counters[2].value;
    }

    increment(index) {
        this.counters[index].value++;
    }
}
