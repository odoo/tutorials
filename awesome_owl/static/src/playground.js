import { Component, useState, markup } from '@odoo/owl';
import { Counter } from './counter/counter';
import { Card } from './card/card';

export class Playground extends Component {
    static template = 'awesome_owl.playground';
    static components = { Counter, Card };

    constructor(props) {
        super(props);
        console.log(
            'calling constructor of own component C in ComponentNode contructor before calling component constructor in owl.js',
        );
    }

    static props = {};

    setup() {
        this.nothing = markup(
            '<h1 style="color:red;">t-out outs markup as markup</h1>',
        );
        this.state = useState({
            c1: 0,
            c2: 0,
        });
    }

    handleCounterChange(counterKey, currentVal) {
        this.state[counterKey] = currentVal;
    }

    get totalSum() {
        return this.state.c1 + this.state.c2;
    }
}
