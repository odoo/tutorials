import { Component,markup,useState } from "@odoo/owl";
import { Counter } from "./components/counter/counter";
import { Card } from "./components/card/card";
import { TodoItem } from "./components/todoitem/todoitem";
import { TodoList } from "./components/todolist/todolist";
export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter,Card,TodoItem,TodoList };
    htmlContent = markup(`
    <p class="text-danger">
        You think <b><i>you</i></b> can
    </p>
`);


    setup(){
        this.state = useState({sum : 0});
    }
    
    handleSum(){

        this.state.sum += 1

    }
    static props = {};
}