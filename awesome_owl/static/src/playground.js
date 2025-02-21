import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };
    setup(){
        this.val3 = "<div class='text-primary'>card3 content</div>"
        this.val4 = markup("<div class='text-primary'>card4 content</div>")
        this.sum = useState({value:2});
    }
    incrementSum(){
        this.sum.value++;
    }
}
