import { useRef, onMounted } from "@odoo/owl";

export function useAutofocus(refName){
    const elementRef = useRef(refName);

    onMounted(() => {
        if(elementRef.el){
            elementRef.el.focus();
        }
    })

    return elementRef;
}
