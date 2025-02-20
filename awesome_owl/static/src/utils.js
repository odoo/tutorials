import {useRef, onMounted} from "@odoo/owl";
export function useAutofocus(refName){
    let inputRef = useRef(refName);
    onMounted(() => {
        console.log(inputRef.el);
        inputRef.el.focus();
    });      
}
