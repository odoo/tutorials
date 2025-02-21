import { Card } from "./card";
import { Counter } from "./counter";
import { Sum } from "./sum";
import { TodoList } from "./todo_list";
import { Component, markup } from "@odoo/owl";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, Sum, TodoList};

    setup(){
        this.cards=[
        { title : "card1", content: "This is normal text"},
        {title : "card2", content: markup("<strong>This is bold text</strong>")},
        {title : "card3", content: "<strong>This is bold text</strong>"},
    ];
    } 
}
