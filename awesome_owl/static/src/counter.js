/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
	static template = "counter";
	static props = { 
		start: Number,
		onChange: {type: Function, optional: true} 
	};

	setup() {
		this.state = useState({ value: this.props.start });
	}

	increment() {
		this.state.value++;
		this.props.onChange?.();
	}
}
