import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup(){
        this.htmlContent = markup("<span style='color:blue; font-weight:700'>some content.</span>")
        this.normalString = "<p style='color:blue>some content.</p>"
        this.state = useState({ sum: 0, isOpen:true });
    }

    incrementSum(){
        this.state.sum++;
    }

    openToggle(){
        if(this.state.isOpen === true)
        {
            this.state.isOpen = false
        }else{
            this.state.isOpen = true
        }
    }
}
