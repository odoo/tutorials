import { Component, useState} from "@odoo/owl";
import { TodoItem } from "../TodoItem/todoitem"; 
import { useAutofocus } from "../../utils";


export class ToDoList extends Component {
    static template = "awesome_owl.todolist";
    static components = { TodoItem };
    setup() {
        this.todos = useState([]);
        this.todoItemsNr =0;
        useAutofocus("todo_input");
    }
    addTodo(inp) {
        if (inp.keyCode === 13) {
            let content = inp.target.value;
            if(content){
                const _newTodo = {
                    id: ++this.todoItemsNr, 
                    description: content,
                    isCompleted: false
                };
                this.todos.push(_newTodo);

            }
            inp.target.value = '';
            this.render();
        }
    }

    toggleState(id) {
        const index = this.todos.findIndex((item) => item.id === id);
        this.todos[index].isCompleted = !this.todos[index].isCompleted;
    }

    removeTodo(id) {
        const index = this.todos.findIndex((item) => item.id === id);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }

}
