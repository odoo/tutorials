import {Component,useState,markup} from "@odoo/owl";
import {Counter} from "./counter/counter";
import {Card} from "./card/card";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card , TodoList};

    setup(){
        this.str1 = markup("<div>some content</div>");
        this.str2 = "<div>some content</div>";
        this.state = useState({ value: 2});
    }

    incrementSum(){
        this.state.value++;
    }
}