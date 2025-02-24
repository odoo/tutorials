/** @odoo-module **/

import { Component, markup } from '@odoo/owl';
import { Counter } from './counter/counter';
import { Card } from './card/card';

export class Playground extends Component {
    static template = 'awesome_owl.playground';
    static components = { Counter, Card };
    static props = {};

    setup() {
        this.escapedValue = "Hello, <b>world</b>!";
        this.notEscapedValue = markup("Hello, <b>world</b>!");
    }
}
