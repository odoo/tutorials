import { Component, useState, xml } from "@odoo/owl"
import { TodoItem } from "./todo_item"
import { TodoInput } from "./todo_input";

export class TodoList extends Component {
    static template = xml`
        <div style="border: 2px solid black; border-radius: 4px; padding: 8px;"> 
            <TodoInput addTodoItem.bind="addTodoItem"/>

            <div t-foreach="state.todos" t-as="todo" t-key="todo.id">
                <TodoItem 
                    id="todo.id"
                    description="todo.description"
                    isCompleted="todo.isCompleted"
                    toggleTodo.bind="toggleTodo"
                    removeTodo.bind="removeTodo"
                />
            </div>
                
        </div>
    `

    static components = { TodoItem, TodoInput} 
    
    setup(){
        this.state = useState({
            todos: [],
            id_counter: 1
        });
    }   

    addTodoItem(newTodoDescription){
        this.state.todos.push({
            id: this.state.id_counter,
            description: newTodoDescription,
            isCompleted:false
        })
        this.state.id_counter++
    }

    toggleTodo(todoId){
        const todo = this.state.todos.find((t) => t.id === todoId)
        if (todo) { todo.isCompleted = !todo.isCompleted }
    }

    removeTodo(todoId){
        const index = this.state.todos.findIndex((t) => t.id === todoId);
        if (index >= 0) {
            this.state.todos.splice(index, 1);
        }
    }
}