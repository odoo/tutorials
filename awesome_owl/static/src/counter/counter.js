/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    // Inline template here so I can specify it directly in xml, other option is to reference an existing template in the XML file.
    static template = "awesome_owl.Counter"

    static props = {
        onChange: { type: Function, optional: true },
    };

    setup() {
        this.state = useState({ value: 0 });
    }

    increment() {
        this.state.value++;

        // To avoid errors when the optional onChange is not passed in as attribute
        if (typeof this.props.onChange !== 'undefined') {
            this.props.onChange();
        }
    }
}
