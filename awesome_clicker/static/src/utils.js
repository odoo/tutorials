export function randomChoice(list) {
    const idx = Math.floor(Math.random() * list.length);
    return list[idx];
}
