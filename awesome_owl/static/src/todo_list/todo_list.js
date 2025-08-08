import { Component, useState, markup } from '@odoo/owl';
import { TodoItem } from '../todo_item/todo_item'

export class TodoList extends Component {
	static template = 'todo_list.todo_list';
	static props = {};
	static components = {TodoItem};

	setup() {
		this.list = useState({items: []});

		this.list.items = JSON.parse(window.localStorage.getItem('todo'));
	}

	update(item) {
		for (let i = 0;i < this.list.items.length;i++) {
			if (this.list.items[i].id == item.id) {
				this.list.items[i].title = item.title;
				this.list.items[i].description = item.description;
				this.list.items[i].isCompleted = item.isCompleted;
			}
		}

		window.localStorage.setItem('todo', JSON.stringify(this.list.items));
	}

	create_task(e) {
		if (e.keyCode != 13) return;
		let newTask = {
			id: 0,
			title: document.getElementById('title').value,
			description: document.getElementById('description').value,
			isCompleted: false,
		}
		
		if (newTask.title == '' || newTask.description == '') return;

		for (let i = 0;i < this.list.items.length;i++) {
			if (this.list.items[i].id >= newTask.id) {
				newTask.id = this.list.items[i].id;
			}
		}
		newTask.id++;
		this.list.items = [...this.list.items, newTask];
		window.localStorage.setItem('todo', JSON.stringify(this.list.items));
		document.getElementById('title').value = '';
		document.getElementById('description').value = '';
	}

	remove(item) {
		const index = this.list.items.findIndex((elt) => elt.id == item.id);
		if (index >= 0) {
			this.list.items.splice(index, 1);
		}


		window.localStorage.setItem('todo', JSON.stringify(this.list.items));
	}
}
