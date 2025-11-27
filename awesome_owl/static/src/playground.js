import { useState, Component } from "@odoo/owl";

export class Playground extends Component {
    static template = "my_module.Counter";

    setup() {
        this.state = useState({ value: 0 });
    }
    
    increment() {
        this.state.value++;
    }
}
