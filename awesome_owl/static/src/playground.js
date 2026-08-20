import { Component, useState, xml, markup } from "@odoo/owl";

import { Counter } from './counter/counter';
import { Card } from './card/card';

export class Playground extends Component {
    setup() {
        this.state = useState({ 
            a: 0,
            b: 0,
            content: markup(`<h1 class="text-danger">hello</h1>`)
        })
    }

    increment_a() {
        this.state.a++
    }

    increment_b() {
        this.state.b++
    }

    static template = xml`
        <div>
            <Counter callback.bind="increment_a" />
            <Counter callback.bind="increment_b" />
        </div>
        
        <br />

        <div>
            <Card title="'Hola'" content="state.content" />
        </div>

        <br />
        
        <div class="p-3">
            Sum:
            <t t-esc="state.a + state.b" />
        </div>
    `

    static components = { Counter, Card }
}
