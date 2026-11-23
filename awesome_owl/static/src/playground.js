import { Component ,markup,useState} from "@odoo/owl";
import { Counter } from "./Counter/counter";
import { Card } from "./Card/card";
import { TodoList } from "./Todo/todoList";



export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = {Counter,Card,TodoList}
    
    HtmlContent = markup('<div>some content</div>')
    setup(){
        this.sum = useState({value:0})
    }

    incrementSum(){
        this.sum.value++;
    }
}
