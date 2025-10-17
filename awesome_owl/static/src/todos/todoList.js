import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todoItem";

export class TodoList extends Component {

    static template = "awesome_owl.todoList";
    static components = { TodoItem };
    
    setup(){
        this.todos = useState([
            { id: 1, description: "read todo", isCompleted: false },
            { id: 2, description: "write tutorial", isCompleted: false },
            { id: 3, description: "buy milk", isCompleted: true }
        ]);

        this.todoInp = useRef("todo_inp");
        
        onMounted(() => {
            this.todoInp.el.focus();
         });
    }
    
    createTodo = (e) => {
        if (e.keyCode===13 && e.target.value!== ''){
            const newId =  Math.floor(Math.random() * 1000);

            this.todos.push({
                id: newId,
                description: e.target.value,
                isCompleted: false
            });

            e.target.value = '';
        }
    }

    toggleState = (id) => {
        const index = this.todos.findIndex((todo) => todo.id === id);
        this.todos[index].isCompleted = !this.todos[index].isCompleted;
    }

    removeTodo = (id) => {
        const index = this.todos.findIndex((todo) => todo.id === id);

        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
