import { Component, useRef, useState } from "@odoo/owl";

export class Calculator extends Component{
    static template = "vanilla_js.Calculator"

    setup(){
        this.output = useState({value:0})
    }

    get first(){
        return document.getElementById('f-input').value;
    }

    get operator(){
        return document.getElementById('o-input').value;
    }

    get second(){
        return document.getElementById('s-input').value;
    }

    calculate(){
        switch (this.operator){
            case "+": this.output.value = Number(this.first) + Number(this.second); break;
            case "-": this.output.value = Number(this.first) - Number(this.second); break;
            case "*": this.output.value = Number(this.first) * Number(this.second); break;
            case "/": this.output.value = Number(this.first) / Number(this.second); break;
            default: this.output.value = "invalid operator"; break;
        }
    }
}
