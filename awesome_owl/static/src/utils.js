import { useRef, onMounted } from "@odoo/owl";

export function useAutoFocus(elementRef){
    const inputRef = useRef(elementRef)
    onMounted(()=> inputRef.el.focus())
}
