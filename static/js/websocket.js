const ws = new WebSocket('ws://localhost:8000/')
const num_medicao = document.getElementById('num_medicao');
const intervalo = document.getElementById('intervalo');
const start_btn = document.getElementById('start_btn');
const pause_btn = document.getElementById('pause_btn');
const stop_btn = document.getElementById('stop_btn');
const restart_btn = document.getElementById('restart_btn');

var output = "";

ws.addEventListener('open', function(event){
    payload = JSON.stringify({device: "client", cmd: ""})
    ws.send(payload)
 });

ws.addEventListener('message', function(event){
    console.log("evento: menssagem recebida")
    const msg = event.data
});

start_btn.addEventListener('click', e => {
    console.log("evento: inicio da medição")
    if (num_medicao.value > 20){
        alert("Valor não aceito, digite um valor entre 1 à 20");
    }
    else{
        output = (num_medicao.value.toString());
        payload = JSON.stringify({
            device: "client",
            num_medicao: Number(num_medicao.value),
            intervalo: Number(intervalo.value),
            cmd:"START"
        })
        ws.send(payload)

        document.querySelector('output').append(output, document.createElement('br'));
    }
})

pause_btn.addEventListener('click', e => {
    console.log("evento: pausa medição")
    payload = JSON.stringify({
        device: "client",
        cmd:"PAUSE"
    })
    ws.send(payload)
})

stop_btn.addEventListener('click', e => {
    console.log("evento: para as medições")
    payload = JSON.stringify({
        device: "client",
        cmd:"STOP"
    })
    ws.send(payload)
})

restart_btn.addEventListener('click', e => {
    console.log("evento: reniciando")
    payload = JSON.stringify({
        device: "client",
        cmd:"RESTART"
    })
    ws.send(payload)
})

