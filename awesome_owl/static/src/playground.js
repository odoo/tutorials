import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter";
import { Card } from "./card";
import { TodoList } from "./todo_list/todo_list";


export class Playground extends Component{
    static template = "awesome_owl.playground";

    static components = { Counter, Card, TodoList };

    setup() {
        this.state = useState({
            sum: 0,
        });

    }

    // card1content = markup("<div> Card 1 content</div>")
    // card2content = "<div> Card 2 content</div>"

    incrementSum() {
        this.state.sum++;
    }

}
