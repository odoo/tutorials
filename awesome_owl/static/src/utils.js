import { useRef, onMounted } from "@odoo/owl";


export function UseAutofocus(refString){
    var myRef = useRef(refString);
    onMounted(() => {
        console.log(myRef.el)
        myRef.el.focus();
    });
}
