import { Component, useState, useRef, onMounted } from "@odoo/owl"
import { ToDoItem } from "../todoitem/todoitem"
import { useAutofocus } from "../utils"

export class ToDoList extends Component{
    static template = "awesome_owl.todolist"
    setup() {
        this.myRef = useRef("my_val")
        useAutofocus(this.myRef)
        this.state = useState({
            todos: [
                { id: 1, description: "Wake up at 6:00 am", isCompleted: true },
                { id: 2, description: "Go to the gym", isCompleted: false },
                { id: 3, description: "Do homework", isCompleted: false },
            ],
            newTodoDescription: "",
        });
        this.changeStatus = this.changeStatus.bind(this);
        this.deleteToDo = this.deleteToDo.bind(this);
    }
    addTodo() {
        if (this.state.newTodoDescription.trim() === "") {
            return;
        }
        const newId = this.state.todos.length + 1; 
        this.state.todos.push({
            id: newId,
            description: this.state.newTodoDescription,
            isCompleted: false,
        });
        this.state.newTodoDescription = ""; 
    }
    keyPress(ev){
        if(ev.keyCode === 13){
            this.addTodo();
        }
    }
    static components = { ToDoItem }
    changeStatus(id){
        const todo = this.state.todos.find((t) => t.id === id);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        } 
    }
    
    deleteToDo(id){
        console.log(id);
        const todo = this.state.todos.find((t) => t.id === id);
        this.state.todos.splice(todo,1);
    }
}
