import { Component , markup , useState  } from "@odoo/owl";
import { Card } from "./card/card";
import { Counter } from "./counter/counter";
import { TodoList } from "./todo_list/todo_list";
export class Playground extends Component {
    
    static template = "awesome_owl.playground";
    static components = { Card , TodoList , Counter  }

    setup() {
        this.str1 = "<div class='text-primary'>some content</div>"
        this.str2 = markup("<div class='text-primary'>some content</div>")
        this.sum = useState({ value:2 }); 
    }  

    incrementSum() {
        this.sum.value++;
    }
}
