/** @odoo-module **/

import { Component , useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";

    static props = ['btnIndex','onchange']

    setup(){
        this.count = useState({value:0});
    }

    do_maths(){
        this.count.value++;
        this.props.onchange();
    }
}
