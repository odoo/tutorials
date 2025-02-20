import {Component, useState }  from "@odoo/owl";
import { Counter } from "./counter";

export class Sum extends Component{
     static template= "estate.Sum";
     static components= { Counter };
    

     setup() {
        this.state = useState({ sum: 0 });
    }

    incrementSum() {
        this.state.sum++;
    }
}
