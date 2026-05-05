import { onMounted, useRef } from "@odoo/owl";

export function useAutofocus(refName){
    const myRef = useRef(refName);
    onMounted(()=>{
        myRef.el.focus();
    })
    return myRef;
}