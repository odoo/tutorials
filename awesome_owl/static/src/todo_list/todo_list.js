import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item"
import { useAutoFocusInput } from "../utils"

export class TodoList extends Component {
	static template = "awesome_owl.TodoList";
	static components = { TodoItem };
	static props = [];


	setup() {
		this.todo_id = 0;
		this.todos = useState([]);
		useAutoFocusInput("input");
	}

	addTodo(ev) {
		if (ev.keyCode !== 13 || ev.target.value.length === 0) {
			return
		}
		this.todos.push({ id: this.todo_id++, description: ev.target.value, isCompleted: false });
		ev.target.value = "";
	}

	toggleTodo(todoId) {
		const todo = this.todos.find(e => e.id === todoId);
		if (todo) {
			todo.isCompleted = !todo.isCompleted;
		}
	}
	removeTodo(todoId) {
		const todo_index = this.todos.findIndex((elem) => elem.id === todoId);
		if (todo_index >= 0) {
			this.todos.splice(todo_index, 1);
		}
	}
}
