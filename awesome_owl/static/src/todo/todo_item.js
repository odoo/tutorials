import { Component, xml } from "@odoo/owl"

export class TodoItem extends Component {
    static template = xml`
        <div t-att-class="props.isCompleted ? 'text-muted text-decoration-line-through' : ''">
            <t t-esc="props.id"/>. <t t-esc="props.description"/>
        </div>
        `

    static props = {
        id: {type: Number},
        description: {type: String},
        isCompleted:  {type: Boolean},
    }


}