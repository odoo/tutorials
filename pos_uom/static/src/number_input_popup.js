import { Component, onMounted, useRef, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class NumberInputPopup extends Component {
    static template = "pos_uom.NumberInputPopup";
    static components = { Dialog };
    static props = {
        title: String,
        getPayload: Function,
        close: Function,
    };
    
    setup() {
        this.inputRef = useRef("input");
        onMounted(this.onMounted);
    }
    onMounted() {
        this.inputRef.el.focus();
        this.inputRef.el.select();
    }
    confirm() {
        if (this.inputRef){
            const configure_success = this.props.getPayload(parseFloat(this.inputRef.el.value));
            if (configure_success){
                this.props.close()
            }
        }
    }

    close() {
        this.props.close();
    }
}
