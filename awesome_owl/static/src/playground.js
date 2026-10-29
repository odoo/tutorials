// import { Component } from "@odoo/owl";

// export class Playground extends Component {
//     static template = "awesome_owl.playground";
// }

import { Component, signal } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    // setup() {
    //     this.state = signal({ value: 0 });
    // }

    // increment() {
    //     this.state.value++;
    // }
    static components = { Counter, Card, TodoList }

    card1 = { title: "card 1", content: "content of card 1" };
    card2 = { title: "card 2", content: "content of card 2" };
    todos = [
        { id: 1, text: "Call the tire garage", completed: true },
        { id: 2, text: "Go to the tire garage", completed: false }
    ];
}