import { Component, useState, useAutofocus, useRef, useEffect, onMounted } from "@odoo/owl";
import { TodoItem } from "../todo_item/todo_item";

export class TodoList extends Component{
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup(){
        this.state = useState({
            todos: [],
            newTask: "",
            taskId: 0
        });
        this.inputRef = useRef("input");
        onMounted(() => {
            this.inputRef.el.focus();
        });
        // useAutofocus("input");
    }

    addTodo(ev){
        if(ev.keyCode === 13){
            const description = this.state.newTask.trim();
            if(description){
                this.state.todos.push({
                    id: this.state.taskId,
                    description: description, 
                    isCompleted: false
                });
                this.state.newTask = "";
                this.state.taskId++;
            }
        }
    }

    toggleState(taskId){
        const todo = this.state.todos.find((t) => t.id === taskId);
        todo.isCompleted = !todo.isCompleted;
    }

    removeTodo(taskId){
        const index = this.state.todos.findIndex((t) => t.id === taskId);

        this.state.todos.splice(index, 1);
    }

    // useAutofocus(name) {
    //     let ref = useRef(name);
    //     useEffect(
    //       (el) => el && el.focus(),
    //       () => [ref.el]
    //     );
    // }      
}
