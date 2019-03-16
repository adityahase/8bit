var App = new Vue({
    el: '#app',
    template: `
        <div class="bg-light">
            <div class="flex">
            <div class="w-1/2 h-screen">
                <h3>Registers</h3>
                <div>A: <input class="border" type="number" v-model.number="registers.A" /></div>
                <div>B: <input class="border" type="number" v-model.number="registers.B" /></div>
                <h3>Memory</h3>
                <div v-for="(m, i) in memory">
                    M : <input class="border" type="number" v-model.number="memory[i]" />
                </div>
            </div>
            <div class="w-1/2 bg-grey-lighter h-screen">
                <div @click="setState(h)" v-for="h in history">
                {{ h.instruction }}
                </div>
                <input class="border" type="text" @keydown.enter="submit">
            </div>
            </div>
        </div>
    `,
    data() {
        return {
            registers: {
                A: 0,
                B: 0
            },
            memory: [0, 0, 0, 0],
            history: []
        }
    },
    methods: {
        async submit(e) {
            const instruction = e.target.value;
            const state = {
                registers: this.registers,
                memory: this.memory,
                program: [instruction]
            };
            const res = await fetch('/emulate', {
                method: 'POST',
                body: JSON.stringify(state)
            });
            if (res.ok) {
                const response = await res.json();
                const laststate = response.slice(-1)[0];
                this.registers = laststate.registers;
                this.memory = laststate.memory;
                this.history.push({
                    instruction,
                    state: {
                        registers: laststate.registers,
                        memory: laststate.memory
                    }
                });
            }
        },
        setState(h) {
            this.registers = h.state.registers;
            this.memory = h.state.memory;
        }
    }
})
