import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter"
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list/todo_list"

export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = { Card, Counter, TodoList };

    static props = {};

    value = markup("<h5 class=\"card-title\">some content</h5>");

    setup() {
        this.sum = useState( {value: 0} );
    }

    incrementSum() {
        this.sum.value++;
    }

}
