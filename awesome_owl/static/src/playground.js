import { Component, useState} from "@odoo/owl";
import { Counter} from "./Components/counter/counter"
import { Card } from "./Components/card/card"
import { TodoList } from "./Components/todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components ={Counter,Card, TodoList}
    setup(){
        this.state = useState({count:0});
    }

    incrementSum(){
        this.state.count++;
    }
    decrementSum()
    {
        if (this.state.count >0)
        {
        this.state.count--;
        }
    }
}