/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter"
import { Card } from "./card"
import { TodoList } from "./todo"

export class Playground extends Component {
	static template = "awesome_owl.playground";
	static components = { Counter, Card, TodoList };

	content1 = markup("<b>Hi World!</b>");
	content2 = markup("<b>Bye World!</b>");

	incrementSum () {
		this.state.sum++;
	}

	setup() {
		this.incrementSum = this.incrementSum.bind(this);
		this.state = useState({ sum: 2 });
	}
}

