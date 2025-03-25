import { useRef, onMounted } from "@odoo/owl";


export function useAutofocus(component, refName = "inputRef") {
    const inputRef = useRef(refName);

    onMounted(() => {
        if (inputRef.el) {
            inputRef.el.focus();
        }
    });

    return inputRef;
}
