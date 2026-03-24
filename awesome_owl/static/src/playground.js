import {Component, onWillStart, useState} from "@odoo/owl";
import {Counter} from "./components/counter/counter";
import {Card} from "./components/card/card";
import {TodoList} from "./components/todo-list/todo-list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = {
        Counter,
        Card,
        TodoList,
    }

    static props = {
        description: {type: String, optional: true},
    }

    setup() {
        this.state = useState({
            sum: 0,
        })

        // For training purposes
        onWillStart(() => {
            this.state.sum = 2;
        });
    }

    incrementSum() {
        this.state.sum++;
    }
}
