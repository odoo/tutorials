import { Component, useState, useRef } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils"

export class TodoList extends Component {
	static template = "awesome_owl.TodoList";
	static components = { TodoItem };

	setup(){
		this.todos = useState([]);
		useAutofocus('input');
	}

	addTodo(ev){
		if (ev.keyCode === 13 && ev.target.value) {
			this.todos.push({
			    id: this.todos.length + 1,
			    description: ev.target.value,
			    isCompleted: false
			});
		}
	}

	inputStatus(todoId) {
		const todo = this.todos.find(item => item.id === todoId);
		todo.isCompleted = !todo.isCompleted;
	}

	removeTodo(todoId){
		const index = this.todos.findIndex(item => item.id === todoId);
		this.todos.splice(index, 1);
	}
}
