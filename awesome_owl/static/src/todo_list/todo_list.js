import { Component, useState } from "@odoo/owl";
import { TodoItem } from "../todo_item/todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
	static template = "awesome_owl.todo_list";
    static components = { TodoItem }; 
    setup() {
		this.todos = useState([]);
        this.nextId = 1; 
		this.inputRef = useAutofocus("input");
    }
    addTodo(ev) {
		if (ev.keyCode === 13) { 
			const input = ev.target;
            const description = input.value.trim();  
			
            if (description) {  
				this.todos.push({
					id: this.nextId++,
                    description: description,
                    isCompleted: false,
                });
                input.value = "";  
				this.inputRef.el.focus();
            }
        }
    }

	toggleTodo(id) {
		this.todos
		.filter((k) => k.id === id)
		.map((k, v) => {
			k.isCompleted = !k.isCompleted;
		});
	}

	removeTodo(id) {
		const index = this.todos.findIndex((todo) => todo.id === id);
		if (index !== -1) {
			this.todos.splice(index, 1);
		} else {
			console.log("Item not found");
		}
	}
}
