import { Component, useState } from "@odoo/owl";
import { TodoItem } from "@awesome_owl/todoItem/todoItem";
import { useAutofocus } from "@awesome_dashboard/utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };
    setup() {
        this.nextId = 1;
        this.todo = useState([]);
        useAutofocus("input")
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value != "") {
            this.todo.push({
                id: this.nextId++,
                description: ev.target.value,
                isCompleted: false
            });
            ev.target.value = "";
        }
    }
    changeIsComplete(changeTodo) {
        changeTodo.isCompleted = !changeTodo.isCompleted;
    }
    removeTodoFromList(todoID) {
        console.log(todoID)
        const index = this.todo.findIndex((elem) => elem.id === todoID);
        console.log(index);
        if(index>=0){
            this.todo.splice(index,1);
        }
        console.log(this.todo);
    }
}