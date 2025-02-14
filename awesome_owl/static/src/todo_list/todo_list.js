import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
	static template = "awesome_owl.todo_list";
	static props = [];
	static components = { TodoItem };

	setup() {
		this.todos = useState([]);
		useAutofocus("todoInput");
	}
	onKeyUpListener(event) {
		if (event.keyCode == "13" && event.target.value) {
			this.todos.push({
				id: this.todos.length + 1,
				description: event.target.value,
				isCompleted: false,
			});
			event.target.value = "";
		}
	}
	toggleState(todoId) {
		const todo = this.todos.find((todo) => todo.id == todoId);
		if (!todo) return;
		todo.isCompleted = !todo.isCompleted;
	}
	removeTodo(todoId) {
		const todoIndex = this.todos.findIndex((todo) => todo.id == todoId);
		if (todoIndex == -1) return;
		this.todos.splice(todoIndex, 1);
	}
}
