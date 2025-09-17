(function monitorLogs() {
    const originalLog = console.log;

    let lastSeen = Date.now();
    let running = true; // flag global para pausar/parar

    // função para parar
    window.fim = function() {
        running = false;
        console.log("✅ Monitor parado manualmente");
    };

    // função para voltar a rodar
    window.inicio = function() {
        if (!running) {
            running = true;
            lastSeen = Date.now();
            console.log("▶ Monitor reiniciado");
        }
    };

    // Call this when your message is detected
    function messageDetected() {
        lastSeen = Date.now();
    }

    // Watchdog loop
    setInterval(() => {
        if (!running) return;

        const elapsed = Date.now() - lastSeen;
        if (elapsed > 114000) {  // mais de 20 segundos
            location.reload();
            lastSeen = Date.now(); // reset after refresh
        }
    }, 1000);

    // Override console.log
    console.log = function (...args) {
        originalLog.apply(console, args); // Ensure other logs still appear

        if (args.some(arg => typeof arg === "string" && arg.includes("Entering battle room"))) {
            messageDetected();
        }
    };

    console.log("Console monitoring started. Use fim() or inicio().");
})();
