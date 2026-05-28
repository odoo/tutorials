import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoItem } from "./todo/todo_item";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoItem, TodoList };

    setup () {
        this.htmlContent = markup("<em style='color:red;'>red text</em>");
        this.normalString = "<b>no markup</b>";
        this.state = useState({counter1: 0, counter2: 0, todoCounter: 0});
    }

    get counterSum () {
        console.log(this.state.counter1, this.state.counter2);
        return this.state.counter1 + this.state.counter2;
    }

    get counterTodo () {
        console.log(this.state.todoCounter)
        return this.state.todoCounter;
    }

    updateCounter1 (count1) {
        this.state.counter1 = count1;
    }

    updateCounter2 (count2) {
        this.state.counter2 = count2;
    }

    updateTodoCounter (todoCount) {
        this.state.todoCounter = todoCount;
    }
}
