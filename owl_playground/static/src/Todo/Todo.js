/** @odoo-module **/
import {Component,useState} from "@odoo/owl";

export class Todo extends Component
{
    static template = "owl_playground.Todo";
    static props = {id : {type:Number},description : {type:String},done:{type:Boolean},toggleState: { type: Function } ,removetodo: {type:Function}};
    onClick(ev) {
        this.props.toggleState(this.props.id);
    }
    remove(ev)
    {
        this.props.removetodo(this.props.id);
    }
}