import { Component, useState, xml } from "@odoo/owl";

export class Counter extends Component {
    static props = { callback: Function }
    
    setup() {
        this.state = useState({ value: 0 })
    }

    increment() {
        this.state.value++
        this.props.callback()
    }

    static template = xml`
        <div>
            <div class="p-3 border rounded">
                <t t-esc="state.value" />
                <button t-on-click="increment" class="btn btn-primary ml-2">
                    +
                </button>
            </div>
        </div>
    `
}
