import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry"
import { StandardFieldProps } from "@web/views/fields/standard_field_props";

export class RatingWidget extends Component {
    static template = "health.RatingWidget"
    static props = {
        ...StandardFieldProps,
    }

    setup() {
        this.degrees = useState([
            { id: 1, value: 1 },
            { id: 2, value: 2 },
            { id: 3, value: 3 },
            { id: 4, value: 4 },
            { id: 5, value: 5 }
        ])
    }

    get recordValue() {
        return this.props.record.data[this.props.name] || 0;
    }

    formatValue(value) {
        return value.toFixed(1);
    }

    updateRecord(newValue) {
        this.props.record.update({ [this.props.name]: newValue })
    }
}

export const ratingWidget = {
    component: RatingWidget,
    supportedTypes: ["integer"]
}

registry.category('fields').add('rating_widget', ratingWidget)
