import { useRef, onMounted } from "@odoo/owl"


export function useAutofocus(ref) {
    const inputRef = useRef(ref);
    onMounted(() => {
        inputRef.el?.focus()
    });
    return inputRef
}