import { Component, markup } from '@odoo/owl';

export class Card extends Component {
	static template = 'card.card';
	static props = {
		title: {
			type: 'String',
			optional: 'true',
		},
		ace: {
			type: 'Function',
			optional: 'true',
		},
		slots: {
			type: 'Object',
			optional: 'true',
		},
	};

	setup() {
		this.title = this.props.title ? this.props.title : 'No Title'; 
		if (this.props.ace) {
			this.props.ace(this);
		}
	}
}
