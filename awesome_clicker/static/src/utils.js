export function choose(array){
    if(array.length === 1){
        return array[0];
    }
    const index = Math.floor(Math.random() * (array.length));
    return array[index];
}
