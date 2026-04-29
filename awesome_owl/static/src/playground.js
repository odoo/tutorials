import {Component, markup, useState} from "@odoo/owl";
import {Counter} from './counter/counter';
import {Card} from './card/card';
import {TodoList} from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static props = {};

    setup() {
        this.state = useState({
            sum: 2,
            todos:[]
        })

        this.incrementSum = this.incrementSum.bind(this)
    }

    incrementSum() {
        this.state.sum++;
    }


    static components = {Counter, Card, TodoList};
}
