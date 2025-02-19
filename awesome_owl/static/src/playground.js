import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";


export class Playground extends Component {
    static template = "awesome_owl.playground";
	static props = [];
	static components = { Counter, Card };
	setup() {
		this.sum = useState({ value: 0 });
	}
	incrementSum() {
		this.sum.value++;
	}
}
