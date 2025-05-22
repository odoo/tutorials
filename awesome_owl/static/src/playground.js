import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        // Example of markup usage
        this.example1 = "<div class='text-primary'>example text</div>";
        this.example2 = markup("<div class='text-primary'>example text</div>");
        
        // Track the total from counters
        this.total = useState({ count: 2 });
    }

    // Increment the total value
    updateTotal() {
        this.total.count++;
    }
}
