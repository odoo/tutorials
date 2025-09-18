import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.state = useState( { value:0 } );
        this.content1 = "<b>hello content1</b>";
        this.content2 = markup("<b>hello content2</b>");
    }

    incrementSum() {
        this.state.value++;
    }

}
