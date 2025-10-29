import {Card} from "./card/card"
import {Component, useState} from "@odoo/owl";
import {Counter} from "./counter/counter";
import {TodoList} from "./todo_list/todo_list";


export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = {Counter, Card, TodoList};

    setup() {
        this.state = useState({sum: 0});
        this.incrementSum = this.incrementSum.bind(this);
    }

    incrementSum() {
        this.state.sum++;
    }
}
