import { Component, useState } from "@odoo/owl"

export class Card extends Component{
    static template = "awesome_owl.card"

    setup(){
        this.toggle = useState({"value": true})
    }

    static props = {
        title: {"type": String, "optional": false},
        slots: {
            "type": Object,
            shape: {
                default: true
            }
        }
    }

    onClick(){
        console.log(this.toggle.value)
        this.toggle.value = !this.toggle.value
        console.log(this.toggle.value)
    }
}
