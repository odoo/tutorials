import { Component, markup } from '@odoo/owl';

export class Card extends Component {
	static template = 'card.card';
	
	setup() {
		this.test_title = "<p>Why do I need to put quotes <em>INSIDE</em> quotes???</p>";
		this.test_content = markup('<p>This limitation of passing the contents of quotation marks as raw javascript is really annoying.</br>I mean, who would want to put quotation marks <em>INSIDE ANOTHER PAIR OF QUOTATION MARKS EVERY SINGLE TIME THEY WANT TO PASS TEXT TO A COMPONENT!</em></br>Though, I guess it could be useful to pass a javascript function to the component.</br>If for whatever reason you wanted to do that.</p>');
		this.title = this.props.title ? this.props.title : this.test_title; 
		this.content = this.props.content ? this.props.content : this.test_content;
		if (this.props.ace) {
			this.props.ace(this);
		}
	}
}
