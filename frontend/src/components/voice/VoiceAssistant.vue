<script setup lang="ts">
/* eslint-disable @typescript-eslint/no-explicit-any */
import { ref } from 'vue';
import intentMap from '@/voice/intent_map.json';

const listening = ref(false);
const transcript = ref('');
const lastResult = ref('');
const sentParams = ref<Record<string, unknown> | null>(null);
const isLoading = ref(false);
const requestUrl = ref<string | null>(null);
const rawResponse = ref<any>(null);
const resultAt = ref<string | null>(null);
const showParams = ref(true);

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
    sentParams.value = null;
    requestUrl.value = null;
    rawResponse.value = null;
    resultAt.value = null;
    isLoading.value = false;
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
        isLoading.value = true;
        try {
            const marketRes = await fetch(apiUrl(mapping.market_endpoint));
            const market = await marketRes.json();
            // call model
            const params = {
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
            };
            sentParams.value = params;
            const qs = buildQuery(params);
            requestUrl.value = `${apiUrl(mapping.endpoint)}?${qs}`;
            const r = await fetch(requestUrl.value);
            const body = await r.json();
            rawResponse.value = body;
            const pred = body.prediction;
            const out = pred ? 'Sí, es probable que suba.' : 'No, probablemente no suba.';
            lastResult.value = `Intención: ${mapping.label}. ${out}`;
            resultAt.value = new Date().toLocaleString();
            speak(lastResult.value);
            return;
        } catch (e) {
            console.warn('voice assistant market/model error', e);
            lastResult.value = 'Error consultando mercado o modelo: ' + String(e);
            speak(lastResult.value);
            return;
        } finally {
            isLoading.value = false;
        }
    }

    // default: use sample params from mapping
    if (mapping.sample_params) {
        isLoading.value = true;
        sentParams.value = mapping.sample_params as Record<string, unknown>;
        const qs = buildQuery(mapping.sample_params);
        try {
            requestUrl.value = `${apiUrl(mapping.endpoint)}?${qs}`;
            const r = await fetch(requestUrl.value);
            const body = await r.json();
            rawResponse.value = body;
            lastResult.value = `Intención: ${mapping.label}. Resultado: ${JSON.stringify(body)}`;
            resultAt.value = new Date().toLocaleString();
            speak(lastResult.value);
            return;
        } catch (e) {
            console.warn('voice assistant model call error', e);
            lastResult.value = 'Error llamando al modelo: ' + String(e);
            speak(lastResult.value);
            return;
        } finally {
            isLoading.value = false;
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
        <div class="voice-card card">
            <div class="card-content">
                <div class="level">
                    <div class="level-left">
                        <div>
                            <h2 class="subtitle">Asistente de voz</h2>
                            <p class="is-size-7">Presiona y di un comando. Ej: "¿Bitcoin va a subir mañana?"</p>
                        </div>
                    </div>
                    <div class="level-right">
                        <div class="buttons are-small">
                            <button class="button is-primary" @click="startListening"
                                :disabled="listening || isLoading">
                                <span class="icon">🔴</span>
                                <span>{{ listening ? 'Escuchando...' : 'Escuchar' }}</span>
                            </button>
                            <button class="button" @click="stopListening">Detener</button>
                        </div>
                    </div>
                </div>

                <div class="columns mt-4">
                    <div class="column is-half">
                        <div class="box">
                            <p class="has-text-weight-semibold">Transcript</p>
                            <p class="is-family-monospace">{{ transcript || '—' }}</p>
                        </div>
                        <div class="box mt-3">
                            <p class="has-text-weight-semibold">Resultado</p>
                            <p>{{ lastResult || '—' }}</p>
                            <p v-if="resultAt" class="is-size-7 has-text-grey">Actualizado: {{ resultAt }}</p>
                        </div>
                    </div>
                    <div class="column is-half">
                        <div class="box">
                            <p class="has-text-weight-semibold">Detalles de la petición</p>
                            <p v-if="isLoading" class="is-size-7 has-text-info">Consultando modelo... <span
                                    class="spinner"></span></p>
                            <p v-if="requestUrl" class="is-size-7"><strong>URL:</strong> <code>{{ requestUrl }}</code>
                            </p>

                            <div v-if="sentParams" class="mt-2">
                                <a class="button is-small is-light" @click.prevent="showParams = !showParams">
                                    {{ showParams ? 'Ocultar parámetros' : 'Mostrar parámetros' }}
                                </a>
                                <div v-show="showParams" class="mt-2 param-box">
                                    <pre>{{ JSON.stringify(sentParams, null, 2) }}</pre>
                                </div>
                            </div>

                            <div v-if="rawResponse" class="mt-3">
                                <p class="has-text-weight-semibold">Respuesta (raw)</p>
                                <pre class="raw-box">{{ JSON.stringify(rawResponse, null, 2) }}</pre>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.voice-card {
    background: #ffffff;
    border-radius: 8px;
    box-shadow: 0 6px 18px rgba(10, 10, 10, 0.08);
}

.spinner {
    display: inline-block;
    width: 14px;
    height: 14px;
    border: 2px solid rgba(0, 0, 0, 0.1);
    border-top-color: #3273dc;
    border-radius: 50%;
    animation: spin 0.9s linear infinite;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

.param-box {
    max-height: 220px;
    overflow: auto;
    background: #f5f7fa;
    padding: 8px;
    border-radius: 4px;
}

.raw-box {
    max-height: 240px;
    overflow: auto;
    background: #0f1720;
    color: #e6eef8;
    padding: 8px;
    border-radius: 4px;
}

.is-family-monospace {
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, 'Roboto Mono', monospace;
}
</style>
