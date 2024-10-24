import {Component, useState} from "@odoo/owl";
import {TodoItem} from "./todoItem";
import {Todos} from "./todos";


export class TodoList extends Component {
    static template = "awesome_owl.TodoList2";
    static components = {TodoItem};
    static props = {}

    setup() {
        let todos = new Todos("Todo List Name");
        todos.add("Buy some milk");
        todos.add("Start next chapter");
        todos.add("Finish this todo List", true);
        this.todoList = useState(todos);

    }

    addTodo(ev) {
        if (ev.keyCode === 13) {
            let txt = ev.target.value.trim();
            if (txt) {
                this.todoList.add(txt);
            }
            ev.target.value = '';
        }
    }
}
