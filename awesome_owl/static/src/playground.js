import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "@awesome_owl/counter/counter";
import { Card } from "@awesome_owl/card/card";
import { TodoList } from "@awesome_owl/todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.str1 = "<div class='text-primary'>this is content 1</div>";
        this.str2 = markup("<div class='text-primary'>this is content 2</div>");
        this.sum = useState({ value: 0 });
    }
    incrementSum() {
        this.sum.value++;
    }
}
