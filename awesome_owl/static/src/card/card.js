import {Component, useState} from '@odoo/owl'

export class Card extends Component {
    static props = {
        title: String,
        slots: { type: Object },
    }

    setup(){
        this.state = useState({
            isOpen: true
        })

        this.props.isOpen = true
        this.toggleOpen = this.toggleOpen.bind(this)
    }

    toggleOpen(){
        console.log(this.state.isOpen);
        this.state.isOpen = !this.state.isOpen
    }

    static template = "awesome_owl.card"

}