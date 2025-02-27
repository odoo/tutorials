import { markup, Component, useState} from "@odoo/owl";
import { Counter } from "./counter/counter.js";
import { Card } from "./card/card.js";
import { ToDoList } from "./todo_list/todo_list.js";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = {Counter, Card, ToDoList};
    
    setup() {
        this.state = useState({ sum: 0 });
        this.normal_content = "<div class='text-primary'>some content</div>"
        this.html_content = markup("<div class='text-primary'>some content</div>")
    }

    incrementSum() {
        this.state.sum += 1;
    }
}
