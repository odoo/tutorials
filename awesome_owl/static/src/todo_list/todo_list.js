import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup(){
        this.todos = useState([]);
        this.todoCount = 1;
        this.inputRef = useRef('taskInput');

        onMounted(()=>{
            this.inputRef.el.focus();
        })
    }

    addTask(e){
        if(e.keyCode === 13 && e.target.value !== ""){
            this.todos.push({
                id: this.todoCount++,
                description: e.target.value,
                isCompleted: false,
            })
            e.target.value = "";
        }
    }

    toggleState(id){
        let todo = this.todos.find((todo) => todo.id === id);
        todo.isCompleted = !todo.isCompleted;
    }

    removeTodo(id){
        const index = this.todos.findIndex((todo) => todo.id === id);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }

}
