import { useRef, onMounted } from "@odoo/owl";

export function useAutoFocus(refElem) {
    const toFocusRef = useRef(refElem);

    onMounted(() => {
        if(toFocusRef.el) {
            toFocusRef.el.focus();
        }
    })    
}
