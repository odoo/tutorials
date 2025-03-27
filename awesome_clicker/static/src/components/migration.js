export const migration = [
    {
        fromVersion: 2,
        toVersion: 3,
        apply: (state) => {
            state.version = 3;
            return state;
        } 
    },
]