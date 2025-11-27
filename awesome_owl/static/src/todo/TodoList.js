import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./TodoItem";


export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };
    setup(){
        this.todos = useState([]);
        this.todoId = 0;
        this.inputRef = useRef("new_task");
        onMounted(() => {
            this.inputRef.el.focus();
        })
    }
    addTodo(e){
        if (e.keyCode === 13){
            if (this.inputRef.el.value){
                this.todoId += 1;
                this.todos.push({ id: this.todoId, description: this.inputRef.el.value, isCompleted: false });
            }
            this.inputRef.el.value = "";
        }
    }
    removeTodo(id){
        const index = this.todos.findIndex(todo => todo.id === id);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
