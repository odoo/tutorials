import { Component, xml } from "@odoo/owl"

export class TodoInput extends Component {
    static template = xml`
        <div>
            <input 
                placeholder="Add a todo"
                t-on-input="_updateInputValue"
                t-on-keyup="ev => this.check(ev)"
            />
            <span t-esc="props.input_val" />
        </div>
    `

    static props = {
        input_val : {type: String}
    }

    _updateInputValue(event) {
        this.props.input_val = event.target.value;
    }

    check(ev) {
        if (ev.keyCode === 13){
            
        }
    }
}