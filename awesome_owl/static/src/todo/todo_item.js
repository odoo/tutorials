import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component {
	static template = "awesome_owl.TodoItem";
	static props = {
		todo: {
			type: Object,
			shape: { id: Number, description: String, isCompleted: Boolean },
		},
		toggle: Function,
        delete: Function,
	};
}
