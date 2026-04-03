import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { Todo } from "./todo/todo";
import { TodoItem } from "./todo_item/todo_item";

export class Playground extends Component {
    static template = "awesome_owl.Playground";
    static components = {Counter, Card, Todo, TodoItem};

    setup() {
        this.state = useState({sum: 0});
        this.htmlContent = markup("<b>This Text is bold</b><br/><i>This Text is Italic</i>");
        this.state = useState({
            sum: 0,
            tasks: []
        });
    }

    incrementSum(value){
        this.state.sum += 1;
    }

    toggleState(id){
        const task = this.state.tasks.find(t => t.id === id);
        if(task){
            task.isCompleted = !task.isCompleted;
        }
    }
}
