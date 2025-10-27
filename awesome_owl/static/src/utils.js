import { useRef, onMounted } from "@odoo/owl";

export function useAutofocus(name) {
    const inputRef = useRef(name);

    onMounted(() => {
        console.log(`focusing on input ${inputRef.el}`);
        inputRef.el.focus()
    })
}
