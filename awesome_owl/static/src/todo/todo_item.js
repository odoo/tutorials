import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component {
	static template = "awesome_owl.TodoItem";
	static props = {
        todo : { type : Object	},
        toggleState : { type : Function},
        removeTodo : { type : Function}
    }

    onChange(todoId) {
    	this.props.toggleState(todoId);
	}

	onRemove(todoId) {
		this.props.removeTodo(todoId);
	}
}