import { Component, onMounted, useRef, useState } from '@odoo/owl'
import { TodoItem } from '../TodoItem/todoitem';


export class TodoList extends Component {
    static template = "awesome_owl/TodoList"
    static components = { TodoItem }

    setup() {
        this.state = useState({ 
            todos: [
                { id: 0, description: "buy Milk", isCompleted:true },                
                { id: 1, description: "Learn Owl", isCompleted: false },
                { id: 2, description: "Build a project", isCompleted: true },
            ],
        });

        this.inputRef = useRef('todoInput')

        onMounted(() => {
            this.inputRef.el.focus();
        })
    }

    addTodo(event) {
        if(event.keyCode == 13) {
            const tododata = event.target.value.trim();
            event.target.value = ''
            console.log(tododata)
            if(tododata != ''){
                this.state.todos.push(
                    {
                        id: this.state.todos.length, 
                        description: tododata, 
                        isCompleted: false
                    }
                )
            }
        }
    }

    toggleStart(todo) {
        todo.isCompleted = !todo.isCompleted
        console.log(todo.isCompleted)
    }

    deleteTodo(todo) {
        console.log(todo.id)
        const index = this.state.todos.findIndex((t) => t.id === todo.id);
        console.log(index)
        if (index >= 0) {
            // remove the element at index from list\
            // console.lo
            this.todos.splice(index, 1);
        }
    }
}
