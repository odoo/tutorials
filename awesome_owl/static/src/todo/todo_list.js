import { Component, useState, xml } from "@odoo/owl"
import { TodoItem } from "./todo_item"
import { TodoInput } from "./todo_input";

export class TodoList extends Component {
    static template = xml`
        <div style="border: 2px solid black; border-radius: 4px; padding: 8px;"> 
            <TodoInput input_val="state.new_todo"/>

            <div t-foreach="state.todos" t-as="todo" t-key="todo.id">
                <TodoItem id="todo.id" description="todo.description" isCompleted="todo.isCompleted"/>
            </div>
                
        </div>
    `

    static components = { TodoItem, TodoInput} 
    
    setup(){
        this.state = useState({
            todos: [
                { id: 1, description: "Go to store", isCompleted: true },
                { id: 3, description: "buy milk", isCompleted: false }
            ],
            new_todo: ""
        });
    }   
}