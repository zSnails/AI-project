<script setup lang="ts">
import { onMounted, ref } from 'vue';

export type Root = {
  faceAttributes: {
    glasses: string
    headPose: {
      pitch: number
      roll: number
      yaw: number
    }
    occlusion: {
      eyeOccluded: boolean
      foreheadOccluded: boolean
      mouthOccluded: boolean
    }
  }
  faceRectangle: {
    height: number
    left: number
    top: number
    width: number
  }
}

const allowed = ref(false);
const canvas = ref<HTMLCanvasElement>();
const photo = ref<HTMLImageElement>();
const video = ref<HTMLVideoElement>();

const width = 320;
let height = 0;
let streaming = false;


onMounted(() => {
  video.value?.addEventListener("canplay", (ev) => {
    ev.preventDefault();
    console.debug("caught canplay event", streaming);
    if (!streaming) {
      if (!video.value || !canvas.value) {
        console.warn("either the video or the canvas is empty");
        return;
      }
      height = video.value?.videoHeight / (video.value?.videoWidth / width);
      console.debug("height", height);
      video.value.setAttribute("width", width.toString());
      video.value.setAttribute("height", height.toString());
      canvas.value.setAttribute("width", width.toString());
      canvas.value.setAttribute("height", height.toString());

      streaming = true;
    }
  });
});

function clearPhoto() {
  if (!canvas.value) return;
  const context = canvas.value?.getContext("2d");
  if (!context) return;
  context.fillStyle = "#aaaaaa";
  context?.fillRect(0, 0, canvas.value?.width, canvas.value?.height);

  const data = canvas.value.toDataURL("image/png");
  photo.value?.setAttribute("src", data);
}

const features = ref<Root[]>([]);
function takePicture() {
  if (!canvas.value || !video.value) {
    console.warn("Either the canvas or the video refs don't have a value set");
    return;
  }
  const context = canvas.value?.getContext("2d");
  console.debug("width", width, "height", height);
  if (width && height) {
    canvas.value.width = width;
    canvas.value.height = height;
    context?.drawImage(video.value, 0, 0, width, height);

    const data = canvas.value.toDataURL("image/png");
    photo.value?.setAttribute("src", data);
    canvas.value.toBlob(async (blob) => {
      if (!blob) return;
      const formData = new FormData();
      formData.append("image", blob, "canvas_image.png");
      const response = await fetch("http://localhost:8080/api/models/face-recognition", {
        method: "POST",
        body: formData
      });
      const result = await response.json();
      console.log(JSON.stringify(result));
      features.value = result.detectedFaces as Root[];
      photo.value?.setAttribute("src", result.resultUrl);
    }, "image/png");
  } else {
    clearPhoto();
    console.info("clearing the photo");
  }
}

async function askPermission() {
  const mediaStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
  if (video.value) {
    console.log(mediaStream);
    video.value.srcObject = mediaStream;
    video.value.play();
  }
  allowed.value = true;
}
</script>
<template>
  <div class="columns">
    <canvas ref="canvas" clas="canvas" hidden></canvas>
    <button @click="askPermission" v-if="!allowed" class="button row">Allow Camera</button>
    <div class="column">
      <div :style="{'display':  allowed ? 'block' : 'none'}">
        <div class="columns">
          <div class="column">
            <video class="row" ref="video">Video Stream Not Available</video>
          </div>
          <div class="column">
            <img src="" alt="The captured image will appear here" ref="photo">
          </div>
        </div>
        <button @click="takePicture" class="button row">Take Image</button>
      </div>
    </div>
    <div class="column">
      <h1 class="title">Found Features</h1>
      <div v-for="(feature, idx) in features">
        <article class="message">
          <div class="message-header">Face {{ idx + 1}}</div>
          <div class="message-body">
            <ul>
              <li>
                <p>{{feature.faceAttributes.glasses}}</p>
              </li>
            </ul>
            <h4 class="title is-6">Glasses</h4>
            <ul>
              <li>
                <p>Eyes fully visible: {{!feature.faceAttributes.occlusion.eyeOccluded}}</p>
                <p>Forehead fully visible: {{!feature.faceAttributes.occlusion.foreheadOccluded}}</p>
                <p>Mouth fully visible: {{!feature.faceAttributes.occlusion.mouthOccluded}}</p>
              </li>
            </ul>
            <h4 class="title is-6">Occlusion</h4>
            <ul>
              <li><pi>Pitch: {{feature.faceAttributes.headPose.pitch}}</pi></li>
              <li><pi>Yaw: {{feature.faceAttributes.headPose.yaw}}</pi></li>
              <li><pi>Roll: {{feature.faceAttributes.headPose.roll}}</pi></li>
            </ul>
            <h4 class="title is-6">Head Pose</h4>
          </div>
        </article>
      </div>
    </div>
  </div>
</template>
