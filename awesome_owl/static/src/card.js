/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";

export class Card extends Component {
	static template = "card";
	static props = {
		'title': {type: String },
		'slots': {type: Object, shape: {default:true} },
	};

	setup() {
		this.state = useState({show: true});
	}
}
