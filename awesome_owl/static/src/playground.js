import {Component, markup, useState} from "@odoo/owl";
import { Card } from "./card/card"
import { Counter } from "./counter/counter"
import { TodoList } from "./todo_list/todo_list"

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Card , Counter, TodoList };

    setup() {
        this.sumOfCounter = useState({value: 2})
    }

    card1Text = '<div class=\'text-primary\'>some content</div>';
    card2Text = markup(this.card1Text);

    incrementSum(){
        this.sumOfCounter.value++;
    }
}
