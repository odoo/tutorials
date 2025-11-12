import { Component, onMounted, useRef, useState } from "@odoo/owl";
import { TodoItem } from "@awesome_owl/TodoItem/todoitem";
import { useAutofocus } from "@awesome_owl/utils";


export class TodoList extends Component {
    static template = "awesome_owl/TodoList";
    static components = { TodoItem };

    setup() {
        this.state = useState({ 
            todos: [
                { id: 0, description: "buy Milk", isCompleted:true },                
                { id: 1, description: "Learn Owl", isCompleted: false },
                { id: 2, description: "Build a project", isCompleted: true },
            ],
        });
        useAutofocus("todoInput");
    }

    addTodo(event) {
        if(event.keyCode == 13) {
            const todoData = event.target.value.trim();
            event.target.value = ''
            if(todoData != ''){
                this.state.todos.push(
                    {
                        id: this.todos.length, 
                        description: todoData, 
                        isCompleted: false
                    }
                )
            }
        }
    }

    toggleStart(todo) {
        todo.isCompleted = !todo.isCompleted;
    }

    deleteTodo(todoId) {
        const index = this.state.todos.findIndex((t) => t.id === todoId);
        if (index >= 0) {
            this.state.todos.splice(index, 1);
            this.state.todos = [ ...this.state.todos ]
        }
    }
}
