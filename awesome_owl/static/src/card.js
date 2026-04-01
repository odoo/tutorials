import { Component, useRef, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        title: String, text: String,
        obj: Object,
        handledone: Function,
        toggle: Function,
        newAdd: Function,
        handledelete: Function,
    }
    setup() {
        //this.newadd(this.newtask_id)
        this.newtask_id = useRef('newtask_id');

        this.handle_the_done = (param) => {
            if (this.props.handledone) {
                this.props.handledone(param);
            }
            else {
                alert("the handle done func is not given");
            }
        }

        this.state = useState({ 'inputnewadd': "" })

        this.newadd_1 = () => {


            this.props.newAdd(this.state.inputnewadd);
        }

        this.handle_the_delete = (param) => {
            this.props.handledelete(param);
        }


        console.log({ "test": this.newtask_id });

    }
}
