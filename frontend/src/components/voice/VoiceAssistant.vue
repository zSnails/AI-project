<script setup lang="ts">
/* eslint-disable @typescript-eslint/no-explicit-any */
import { ref } from 'vue';
import intentMap from '@/voice/intent_map.json';

const listening = ref(false);
const transcript = ref('');
const lastResult = ref('');

let recognition: any = null;
const SpeechRecognitionClass: any = (window as unknown as any).SpeechRecognition || (window as unknown as any).webkitSpeechRecognition;
if (SpeechRecognitionClass) {
    recognition = new SpeechRecognitionClass();
    recognition.lang = 'es-ES';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    recognition.onresult = (ev: any) => {
        const text = ev.results[0][0].transcript;
        transcript.value = text;
        processTranscript(text);
    };
    recognition.onend = () => {
        listening.value = false;
    };
}

function startListening() {
    if (!recognition) {
        alert('SpeechRecognition no está disponible en este navegador');
        return;
    }
    transcript.value = '';
    lastResult.value = '';
    listening.value = true;
    recognition.start();
}

function stopListening() {
    if (recognition) recognition.stop();
    listening.value = false;
}

function speak(text: string) {
    const u = new SpeechSynthesisUtterance(text);
    u.lang = 'es-ES';
    speechSynthesis.speak(u);
}

function detectIntent(text: string): string | null {
    const t = text.toLowerCase();
    for (const key of Object.keys(intentMap)) {
        const entry = (intentMap as unknown as any)[key] as { keywords?: string[] };
        for (const kw of entry.keywords || []) {
            if (t.includes(kw.toLowerCase())) return key;
        }
    }
    return null;
}

function buildQuery(params: Record<string, unknown>) {
    const ps = new URLSearchParams();
    for (const k of Object.keys(params)) ps.append(k, String(params[k] ?? ''));
    return ps.toString();
}

function apiUrl(path: string) {
    // If the path is an absolute URL, return as-is
    if (/^https?:\/\//.test(path)) return path;
    // If frontend is served from the same host/port as backend, use relative
    try {
        const loc = window.location;
        // If current origin is same as backend origin (port 8080), use relative
        if (loc.port === '8080' || loc.hostname === 'localhost' && loc.port === '8080') {
            return path;
        }
    } catch (e) {
        console.log('apiUrl error', e);
    }
    // Otherwise, default to backend running on localhost:8080
    return `http://localhost:8080${path}`;
}

async function processTranscript(text: string) {
    const intent = detectIntent(text);
    if (!intent) {
        lastResult.value = 'No pude identificar la intención. Dime: "Bitcoin" o "Aguacate"...';
        speak(lastResult.value);
        return;
    }

    const mapping = (intentMap as unknown as any)[intent] as Record<string, any>;

    // bitcoin special flow: fetch market snapshot if requested
    if (mapping.requires_latest_data && mapping.market_endpoint) {
        try {
            const marketRes = await fetch(apiUrl(mapping.market_endpoint));
            const market = await marketRes.json();
            // call model
            const qs = buildQuery({
                open: market.open,
                high: market.high,
                low: market.low,
                close: market.close,
                volume: market.volume,
                'market-cap': market.market_cap,
                return: market.return,
                ma3: market.ma3,
                ma7: market.ma7,
                volatility: market.volatility,
            });
            const r = await fetch(`${apiUrl(mapping.endpoint)}?${qs}`);
            const body = await r.json();
            const pred = body.prediction;
            const out = pred ? 'Sí, es probable que suba.' : 'No, probablemente no suba.';
            lastResult.value = `Intención: ${mapping.label}. ${out}`;
            speak(lastResult.value);
            return;
        } catch (e) {
            console.warn('voice assistant market/model error', e);
            lastResult.value = 'Error consultando mercado o modelo: ' + String(e);
            speak(lastResult.value);
            return;
        }
    }

    // default: use sample params from mapping
    if (mapping.sample_params) {
        const qs = buildQuery(mapping.sample_params);
        try {
            const r = await fetch(`${apiUrl(mapping.endpoint)}?${qs}`);
            const body = await r.json();
            lastResult.value = `Intención: ${mapping.label}. Resultado: ${JSON.stringify(body)}`;
            speak(lastResult.value);
            return;
        } catch (e) {
            console.warn('voice assistant model call error', e);
            lastResult.value = 'Error llamando al modelo: ' + String(e);
            speak(lastResult.value);
            return;
        }
    }

    lastResult.value = 'No hay parámetros definidos para este intent.';
    speak(lastResult.value);
}
</script>

<template>
    <div>
        <h1 class="title">Asistente de voz</h1>
        <p>Presiona el botón y di el comando. Ejemplos: "¿Bitcoin va a subir mañana?", "Predice el precio del aguacate"
        </p>
        <div class="buttons">
            <button class="button is-primary" @click="startListening" :disabled="listening">Start</button>
            <button class="button" @click="stopListening">Stop</button>
        </div>
        <div class="box">
            <p><strong>Transcript:</strong> {{ transcript }}</p>
            <p><strong>Resultado:</strong> {{ lastResult }}</p>
        </div>
    </div>
</template>
