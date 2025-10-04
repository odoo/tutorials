import { Component, useState } from "@odoo/owl";


export class Card extends Component {
	static template = "awesome_owl.card";
	static props = {
		title: { type: String },
		content: String,
        slots: {
            type: Object,
            shape: {
                default: true
            },
        }
	};
	setup() {
		this.showContent = useState({ value: true });
	}
	toggleContent() {
		this.showContent.value = !this.showContent.value;
	}
}
