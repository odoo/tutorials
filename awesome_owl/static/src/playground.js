/** @odoo-module **/

const { markup, Component, useState } = owl;
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo_list/todo_list";


export class Playground extends Component {
    static template = "awesome_owl.playground";

    title_1 = markup('<h5 class="card-title">Title 1</h5>')
    title_2 = markup('<h5 class="card-title">Title 2</h5>')
    sum = useState({ value: 0 });

    incrementSum() {
        this.sum.value++;
    }
    static components = { Counter, Card, TodoList };
}


