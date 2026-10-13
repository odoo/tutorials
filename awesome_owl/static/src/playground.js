import {Component, markup, useState} from "@odoo/owl";
import {Counter} from "./counter/counter";
import {Card} from "./card/card";
import {TodoList} from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = {Counter, Card};

    setup() {
        this.safeHtml = markup("<span class='text-success fw-bold'>This is real HTML</span>");
        this.unsafeString = "<span class='text-danger'>Hello</span>";
        this.state = useState({sum: 2});
    }

    incrementSum() {
        this.state.sum++;
    }

}
