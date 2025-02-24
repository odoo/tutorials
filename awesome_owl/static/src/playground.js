/** @odoo-module **/

import { Component, markup , useState} from "@odoo/owl";


export class Playground extends Component {
    static template = "awesome_owl.playground";

    setup() {
        this.state = useState({
            value: 0,
        })
    }

    increment() {
        this.state.value++
    }

    decrement() {
        this.state.value--
    }

    reset() {
        this.state.value = 0
    }
    

}
