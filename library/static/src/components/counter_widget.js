import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry"
import { StandardFieldProps } from "@web/views/fields/standard_field_props";

export class CounterWidget extends Component {
    static template = "library.CounterWidget";
    static props = {
        ...StandardFieldProps,
    }

    setup() {
        this.degrees = useState([
            { id: 1, value: 1 },
            { id: 2, value: 10 },
            { id: 3, value: 100 },
            { id: 4, value: 1000 }
        ])
        this.state = useState({ degree: 1 })
    }

    get recordValue() {
        return this.props.record.data[this.props.name] || 0;
    }

    updateRecord(newValue) {
        this.props.record.update({ [this.props.name]: newValue })
    }

    onChangeDegree(ev) {
        this.state.degree = Number(ev.target.value)
    }


    increment() {
        this.updateRecord(this.recordValue + this.state.degree)
    }

    decrement() {
        this.updateRecord(this.recordValue - this.state.degree)
    }

}

export const counterWidget = {
    component: CounterWidget,
    supportedTypes: ["float", "integer", "monetary"],
}

registry.category('fields').add('counter_widget', counterWidget)
