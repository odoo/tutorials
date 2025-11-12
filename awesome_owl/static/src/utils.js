import { onMounted, useRef } from "@odoo/owl";


export function useAutoFocus(refName){
    const elementRef = useRef(refName);
    onMounted(() =>{
        if(elementRef.el){
            elementRef.el.focus();
        }
    });
    return elementRef;
}
