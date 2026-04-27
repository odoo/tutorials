import { markup, Component, useState } from "@odoo/owl";
import { Counter } from "./counter/counter"
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static components = {
        Counter, 
        Card,
        TodoList,
    };

    static template = "awesome_owl.playground";

    setup(){
        this.html = markup("<div class='text-info'>some text 2</div>")
        this.sum = useState({value:0});
    }

    incrementSum(){
        this.sum.value++;
    }
    
    decrementSum(){
        this.sum.value--;
    }
}
