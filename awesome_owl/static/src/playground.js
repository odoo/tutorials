/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo-list/todo-list";


export class Playground extends Component {
	static template = "awesome_owl.playground";
	static components = { Counter, Card, TodoList };


	setup() {
		this.value1 = "<div>some text 1</div>";
		this.value2 = markup("<div>some text 2</div>");
		this.sum = useState({ value: 0 });
	}

	increment() {
		this.sum.value++;
	}
}
