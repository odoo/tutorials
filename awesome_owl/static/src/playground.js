import { Component, markup , useState} from "@odoo/owl";
import { Card } from "./card/card"; // Import the Card component
import { Counter } from "./counter/counter";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Card , Counter, TodoList };
    setup() {
        this.htmlContent = markup("<div class='text-primary'>some content</div>");
        this.state = useState({ sum : 0 });
        this.incrementSum = this.incrementSum.bind(this);
    }

    incrementSum() {
        this.state.sum ++;
    }
    
}

