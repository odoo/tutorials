import { Component, markup, useState } from "@odoo/owl";
import { TodoList } from '@awesome_owl/todo/todo_list';
import { Card } from '@awesome_owl/card/card';
import { Counter } from '@awesome_owl/counter/counter';
import { TodoItem } from '@awesome_owl/todo/todo_item';

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = {TodoList, Card, Counter , TodoItem};
    setup(){
     this.state = useState({ sum: 0 });
    }

    incrementSum() {
        this.state.sum++;
    }
}
