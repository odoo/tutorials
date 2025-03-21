/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from './counter/counter';
import { Card } from './card/card';
import { TodoList } from './todo_list/todo_list';

export class Playground extends Component {
	static template = "awesome_owl.playground";
	static components = { Counter, Card, TodoList };
	static props = {};

	setup() {
		this.counter = useState({value: 0});
	}


	updateTotal(str) {
		this.counter.value++;
	}
}
