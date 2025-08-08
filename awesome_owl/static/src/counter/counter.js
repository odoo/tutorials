import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
	static template = 'counter.counter';
	static props = {
		onChange: {type: 'Function', optional: 'true',},
	}
	setup() {
		this.counter = useState({value: 0});
	}

	increment() {
		this.counter.value++;
		this.props.onChange('Prout!');
	}
}
