import { markup, Component, useState } from "@odoo/owl";
import { Counter } from "./components/counter/counter";
import { Card } from "./components/card/card";
import { TodoList } from "./components/todo/todoList";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = {Counter, Card, TodoList}
    
    html = markup("<div>Some Content</div>")

    setup(){
        this.state = useState({
            sum:2
        })
    }

    sumCounter(){
        this.state.sum++;
    }
}
