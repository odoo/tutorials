/** @odoo-module **/

import { TodoList } from "./components/todo_list";

import { Component, useState, xml, markup } from "@odoo/owl";

export class Counter extends Component {
    static props = {
        onChange: { type: Function, optional: true },
    };

    static template = xml`
        <div>
            Counter:
            <t t-esc='state.value'/>
            <button t-on-click="increment">Increment</button>
        </div>
    `;

    setup() {
        this.state = useState({ value: 0 });
    }

    increment() {
        this.state.value++;
        if (this.props.onChange) {
            this.props.onChange()
        }
    }
}

export class Card extends Component {
    static props = ['title', 'slots?'];

    setup() {
        this.state = useState({ visible: true });
    }

    static template = xml`
        <div class="card d-inline-block m-2" style="width: 18rem;">
            <div class="card-body">
                <h5 class="card-title"><t t-out='props.title'/></h5>
                <button t-on-click="turnOfCard">Toggle</button>
                <t t-slot="default" t-if="state.visible"/>
            </div>
        </div>`;

    turnOfCard() {
        this.state.visible = !this.state.visible;
    }
}

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.content1 = markup("<div>some text 2</div>");
        this.content2 = markup("<div>some text 2</div>");
        this.state = useState({ sum: 0 });
    }

    updateSum() {
        this.state.sum++;
    }
}

