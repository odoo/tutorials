import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./TodoList/TodoList";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };
    static props = {};
    todo = {id: 3, description: "buy milk", isCompleted: false };
    html = markup("<h1> Hi </h1>");

    setup()
    {
        this.sum = useState({value: 0});
    }
    incrementSum()
    {
        this.sum.value ++;
    }

    
}
