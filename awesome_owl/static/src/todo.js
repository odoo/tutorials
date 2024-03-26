/** @odoo-module **/

import { Component, onMounted, useRef, useState } from "@odoo/owl";
import { useAutoFocus } from "./utils"

export class TodoItem extends Component {
	static template = "todo_item";
	static props = {
		todo: {
			type: Object, 
			shape: { id: Number, description: String, isCompleted: Boolean }
		},
		toggleState: { type: Function, optional: true },
		removeItem: { type: Function},
	}
	testmeth() {
		console.log("foo");
	}
}


export class TodoList extends Component {
	static template = "todo_list";
	static components = { TodoItem };

	nextId = 0;
	setup() {
// 		this.toggleTodo = this.toggleTodo.bind(this);
		this.addTodo = this.addTodo.bind(this);
		this.todos = useState([]);
		useAutoFocus("todo_input");
	}

	addTodo(ev) {
		if (!(ev.keyCode == 13) || ev.target.value == '') {
			return ;
		}
		this.todos.push({id: this.nextId, description: ev.target.value, isCompleted: false});
		ev.target.value = "";
		this.nextId++;
	}

	toggleTodo(ev, i) {
		this.todos[i].isCompleted = ev.target.checked;
	}

	removeTodo(ev, i) {
		console.log("rm", i)
		this.todos.splice(i, 1);
	}
}

// export class TodoItem extends Component {
// 	static template = "todo_item";
// 	static props = {
// 		todo: {
// 			type: Object, 
// 			shape: { id: Number, description: String, isCompleted: Boolean }
// 		},
// 	}
// 
// 	setup() {
// 		this.change = this.change.bind(this);
// 		this.todo = useState({id: -1, description: '', isCompleted: false})
// 		onMounted( () => {
// 			this.todo = this.props.todo;
// 		})
// 	}
// 
// 	change(ev) {
// 		this.todo.isCompleted = ev.target.checked;
// 	}
// }
// 
// export class TodoList extends Component {
// 	static template = "todo_list";
// 	static components = { TodoItem };
// 
// 	nextId = 0;
// 	setup() {
// 		this.addTodo = this.addTodo.bind(this);
// 		this.todos = useState([]);
// // 		this.inputRef = useRef("todo_input");
// // 		onMounted( () => {
// // 			this.inputRef.el.focus();
// // 		});
// 		useAutoFocus("todo_input");
// 	}
// 
// 	addTodo(ev) {
// 		if (!(ev.keyCode == 13) || ev.target.value == '') {
// 			return ;
// 		}
// 		this.todos.push({id: this.nextId, description: ev.target.value, isCompleted: false});
// 		ev.target.value = "";
// 		this.nextId++;
// 	}
// 
// // 	toggleTodo(ev, i) {
// // 		this.todos[i].isCompleted = ev.target.checked;
// // 	}
// // 
// }
