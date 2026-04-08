import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todolist/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.state = useState({ c_sum: 0 });
    }

    incrementSum(){
        this.state.c_sum++;
    }

    card1_content = '<div class="text-primary">Some Text</div>';
    card2_content = markup('<div class="text-primary">Some Text</div>');
}
