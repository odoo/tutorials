import { Component, useState } from '@odoo/owl';

export class TodoItem extends Component {
	static template = 'todo_item.todo_item';
	static props = {
		id: {type: 'Number',},
		title: {type: 'String', optional: 'true',},
		description: {type: 'String', optional: 'true',},
		isCompleted: {type: 'Boolean', optional: 'true',},
		update: {type: 'Function',},
		remove: {type: 'Function',},
	}
	setup() {
		this.contents = useState({
			id: this.props.id,
			title: this.props.title ? this.props.title : 'No Title.',
			description: this.props.description ? this.props.description : 'No Description.',
			isCompleted: this.props.isCompleted,
		});

	}

	click() {
		this.contents.isCompleted = !this.contents.isCompleted;
		this.props.update(this.contents);
	}

	rubbish_bin() {
		this.props.remove(this.contents);
	}
}
