// Nhân vật 3D dựng bằng code (có khớp đùi/chân, thân, đầu, 2 tay) — biết ĐỨNG DẬY, ĐI BỘ theo đường NavGrid,
// GIAO TIẾP TRÒ CHUYỆN (vung tay, gật đầu trao đổi công việc), GÕ PHÍM và XIN DUYỆT QUYỀN.
import * as THREE from 'three';
import { paint, combine, hash, rbox } from './util.js';

const SKIN = ['#f1d3b8', '#e8c19f', '#d9a982', '#c48b62', '#a46f4b', '#7c5236'];
const HAIR = ['#1d1a18', '#2e2620', '#4a3424', '#6b4a2e', '#8c6a46', '#262a33', '#b58a5a'];
const SHIRT = ['#10b981', '#6366f1', '#ec4899', '#f59e0b', '#06b6d4', '#3c4250', '#c9a24a', '#e7dfd0', '#4f46e5', '#0ea5e9'];
const PANTS = ['#2a2c31', '#3c3f46', '#4a4237', '#1f2a3d', '#5d5a52'];
const SHOES = ['#f0ede8', '#26272b', '#5a4634'];

const wrapAngle = (a) => Math.atan2(Math.sin(a), Math.cos(a));
const lerpAngle = (a, b, k) => a + wrapAngle(b - a) * k;
const yawOf = (dx, dz) => Math.atan2(-dx, -dz);

/** Phần thân trên (hông + áo + cổ) */
function torsoGeo(look) {
  const parts = [];
  const cap = (r, l, col) => paint(new THREE.CapsuleGeometry(r, l, 4, 10), col);
  parts.push({ geo: paint(new THREE.SphereGeometry(0.165, 12, 8), look.pants), y: 0.04, z: 0.01, s: [1.14, 0.58, 0.92] });
  parts.push({ geo: cap(0.155, 0.28, look.shirt), y: 0.32, z: 0.01, rx: -0.06, s: [1.22, 1, 0.8] });
  parts.push({ geo: paint(new THREE.CylinderGeometry(0.045, 0.05, 0.1, 8), look.skin), y: 0.6, z: -0.02 });
  return combine(parts);
}

/** 1 bên chân (gốc ở khớp hông): khi đứng thẳng duỗi dọc xuống -y; khi ngồi xoay khớp gối hoặc nghiêng đùi */
function legUpperGeo(look) {
  const cap = (r, l, col) => paint(new THREE.CapsuleGeometry(r, l, 4, 8), col);
  return combine([
    { geo: cap(0.074, 0.26, look.pants), y: -0.16, z: 0 },
  ]);
}

function legLowerGeo(look) {
  const cap = (r, l, col) => paint(new THREE.CapsuleGeometry(r, l, 4, 8), col);
  return combine([
    { geo: cap(0.062, 0.28, look.pants), y: -0.17, z: 0 },
    { geo: paint(rbox(0.098, 0.068, 0.21, 0.03), look.shoe), y: -0.34, z: -0.04 },
  ]);
}

function headGeo(look) {
  const parts = [];
  parts.push({ geo: paint(new THREE.SphereGeometry(0.108, 18, 14), look.skin), y: 0.1, s: [0.95, 1.05, 1] });
  const top = paint(new THREE.SphereGeometry(0.117, 18, 10, 0, Math.PI * 2, 0, look.style === 3 ? 0.9 : 1.2), look.hair);
  parts.push({ geo: top, y: 0.11 });
  if (look.style !== 3) parts.push({ geo: paint(new THREE.SphereGeometry(0.118, 16, 10, 0, Math.PI, 0, 2.1), look.hair), y: 0.105, z: 0.004 });
  if (look.style === 1) parts.push({ geo: paint(new THREE.CapsuleGeometry(0.075, 0.16, 4, 10), look.hair), y: -0.02, z: 0.07, s: [1.4, 1, 0.6] });
  if (look.style === 2) parts.push({ geo: paint(new THREE.SphereGeometry(0.052, 12, 8), look.hair), y: 0.2, z: 0.08 });
  for (const sx of [-1, 1]) parts.push({ geo: paint(new THREE.SphereGeometry(0.024, 8, 6), look.skin), x: sx * 0.102, y: 0.1, z: 0.005, s: [0.5, 1, 0.8] });
  return combine(parts);
}

function armGeo(look) {
  const parts = [];
  const cap = (r, l, col) => paint(new THREE.CapsuleGeometry(r, l, 4, 8), col);
  parts.push({ geo: cap(0.052, 0.2, look.shirt), y: -0.13, z: -0.02, rx: 0.15 });
  parts.push({ geo: cap(0.044, 0.3, look.sleeve), y: -0.235, z: -0.2, rx: Math.PI / 2 - 0.12 });
  parts.push({ geo: paint(rbox(0.07, 0.03, 0.09, 0.012), look.skin), y: -0.2, z: -0.42 });
  return combine(parts);
}

const AGENT_SHIRT_OVERRIDE = {
  'mama': '#10b981',
  'mkt': '#6366f1',
  'content': '#8b5cf6',
  'edit': '#ec4899',
  'edit-2': '#f43f5e',
  'voice': '#d946ef',
  'content-da-kenh': '#f59e0b',
  'quan-ly-kenh': '#eab308',
  'cham-soc-kenh': '#f97316',
  'hieu-suat': '#06b6d4',
  'bo-nao-thu-2': '#0ea5e9',
};

export function lookFor(id) {
  const h = hash(id);
  const pick = (arr, k) => arr[(h >>> k) % arr.length];
  const shirt = AGENT_SHIRT_OVERRIDE[id] || pick(SHIRT, 3);
  const shortSleeve = ((h >>> 21) & 3) === 0;
  const skin = pick(SKIN, 0);
  return { skin, hair: pick(HAIR, 7), shirt, sleeve: shortSleeve ? skin : shirt, pants: pick(PANTS, 11), shoe: pick(SHOES, 15), style: (h >>> 18) % 4 };
}

export class Person {
  constructor(id) {
    this.id = id;
    this.look = lookFor(id);
    this.mat = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.72, transparent: false });
    this.root = new THREE.Group();
    this.body = new THREE.Mesh(torsoGeo(this.look), this.mat);
    this.headPivot = new THREE.Group();
    this.headPivot.position.set(0, 0.64, -0.02);
    this.head = new THREE.Mesh(headGeo(this.look), this.mat);
    this.headPivot.add(this.head);

    this.arms = [-1, 1].map(sx => {
      const pivot = new THREE.Group();
      pivot.position.set(sx * 0.2, 0.5, -0.02);
      pivot.add(new THREE.Mesh(armGeo(this.look), this.mat));
      this.root.add(pivot);
      return pivot;
    });

    // 2 chân có khớp hông (hip) và khớp gối (knee) để vừa ngồi ghế vừa đứng dậy đi bộ mượt mà
    this.legs = [-1, 1].map(sx => {
      const hip = new THREE.Group();
      hip.position.set(sx * 0.1, 0.02, 0);
      const upper = new THREE.Mesh(legUpperGeo(this.look), this.mat);
      const knee = new THREE.Group();
      knee.position.set(0, -0.30, 0);
      const lower = new THREE.Mesh(legLowerGeo(this.look), this.mat);
      knee.add(lower);
      hip.add(upper, knee);
      this.root.add(hip);
      return { hip, knee };
    });

    this.root.add(this.body, this.headPivot);
    this.root.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } o.userData.dynamic = true; });
    this.status = 'idle';
    this.talking = false;
    this.phase = (hash(id) % 1000) / 1000 * Math.PI * 2;
    this.pose = { type: 0, raise: 0, lap: 1, down: 0, talk: 0, walk: 0 };
    this.anchor = new THREE.Vector3();
    this.standing = 0;
    this.canWalk = true;
    this.trip = null;
    this.walkCycle = 0;
  }

  /** Di chuyển thật theo đường đi NavGrid: đứng dậy -> đi bộ qua các điểm -> ngồi xuống hoặc đứng nói chuyện */
  travel({ path, seat, run = false, standAtEnd = false, onArrive }) {
    this.variant = seat.variant ?? 'desk';
    if (!path || path.length < 2) {
      this.trip = null;
      this.standing = standAtEnd ? 1 : 0;
      this.place(seat.x, standAtEnd ? 0.68 : (seat.seatH ?? 0.5), seat.z, seat.facing ?? 0);
      onArrive?.();
      return;
    }
    const pts = path.map(p => ({ x: p.x, z: p.z }));
    if (!standAtEnd) pts.push({ x: seat.x, z: seat.z });
    this.trip = {
      pts,
      idx: 0,
      seat,
      speed: run ? 2.85 : 1.75,
      standAtEnd,
      stage: this.standing < 0.8 ? 'stand' : 'walk',
      timer: 0,
      onArrive,
    };
  }

  setStatus(s) {
    this.status = s;
    const off = s === 'offline';
    this.mat.transparent = off;
    this.mat.opacity = off ? 0.35 : 1;
    this.mat.depthWrite = !off;
    this.mat.emissive.set(s === 'error' ? '#3a0606' : '#000000');
    this.mat.needsUpdate = true;
  }

  update(t, dt) {
    // 1. Xử lý hành trình đi bộ (trip)
    let isWalking = false;
    if (this.trip) {
      const tr = this.trip;
      if (tr.stage === 'stand') {
        tr.timer += dt / 0.32;
        this.standing = Math.min(1, tr.timer);
        const startPt = tr.pts[0];
        this.anchor.x += (startPt.x - this.anchor.x) * Math.min(1, dt * 8);
        this.anchor.z += (startPt.z - this.anchor.z) * Math.min(1, dt * 8);
        this.root.position.set(this.anchor.x, (this.baseY ?? 0.5) * (1 - this.standing) + 0.68 * this.standing, this.anchor.z);
        if (tr.timer >= 1) { tr.stage = 'walk'; tr.timer = 0; }
      } else if (tr.stage === 'walk') {
        isWalking = true;
        const targetPt = tr.pts[Math.min(tr.idx + 1, tr.pts.length - 1)];
        const dx = targetPt.x - this.anchor.x;
        const dz = targetPt.z - this.anchor.z;
        const dist = Math.hypot(dx, dz);
        const step = tr.speed * dt;
        if (dist > 0.02) {
          const desiredYaw = yawOf(dx, dz);
          this.root.rotation.y = lerpAngle(this.root.rotation.y, desiredYaw, Math.min(1, dt * 12));
        }
        if (dist <= step || tr.idx + 1 >= tr.pts.length) {
          this.anchor.x = targetPt.x;
          this.anchor.z = targetPt.z;
          tr.idx++;
          if (tr.idx >= tr.pts.length - 1) {
            tr.stage = tr.standAtEnd ? 'done_stand' : 'sit';
            tr.timer = 0;
          }
        } else {
          this.anchor.x += (dx / dist) * step;
          this.anchor.z += (dz / dist) * step;
        }
        this.walkCycle += dt * tr.speed * 5.8;
        const bob = Math.abs(Math.sin(this.walkCycle)) * 0.038;
        this.root.position.set(this.anchor.x, 0.68 + bob, this.anchor.z);
      } else if (tr.stage === 'sit') {
        tr.timer += dt / 0.32;
        this.standing = Math.max(0, 1 - tr.timer);
        const sh = tr.seat.seatH ?? 0.5;
        this.baseY = sh;
        this.anchor.x = tr.seat.x;
        this.anchor.z = tr.seat.z;
        this.root.rotation.y = lerpAngle(this.root.rotation.y, tr.seat.facing ?? 0, Math.min(1, dt * 12));
        this.root.position.set(tr.seat.x, sh * (1 - this.standing) + 0.68 * this.standing, tr.seat.z);
        if (tr.timer >= 1) {
          this.standing = 0;
          this.place(tr.seat.x, sh, tr.seat.z, tr.seat.facing ?? 0);
          const cb = tr.onArrive;
          this.trip = null;
          cb?.();
        }
      } else if (tr.stage === 'done_stand') {
        this.standing = 1;
        this.root.rotation.y = tr.seat.facing ?? this.root.rotation.y;
        this.root.position.set(tr.seat.x, 0.68, tr.seat.z);
        const cb = tr.onArrive;
        this.trip = null;
        cb?.();
      }
    }

    const s = this.status;
    const target = {
      type: !isWalking && this.standing < 0.2 && s === 'working' && !this.talking ? 1 : 0,
      raise: !isWalking && s === 'waiting' ? 1 : 0,
      lap: !isWalking && !this.talking && (s === 'idle' || s === 'queued' || s === 'error' || s === 'offline') ? 1 : 0,
      down: s === 'error' ? 1 : 0,
      talk: !isWalking && this.talking ? 1 : 0,
      walk: isWalking ? 1 : 0,
    };
    const k = Math.min(1, dt * 6);
    for (const key in target) this.pose[key] += (target[key] - this.pose[key]) * k;
    const p = this.pose, ph = this.phase;
    if (s === 'offline') return;

    // 2. Xương chân: ngồi ghế (hip gập +90 độ hướng về -z, gối gập -90 độ xuống đất) vs đứng/đi bộ
    const sitFactor = 1 - this.standing;
    const [legL, legR] = this.legs;
    const swing = Math.sin(this.walkCycle) * 0.62 * p.walk;
    legL.hip.rotation.x = sitFactor * (Math.PI / 2) + swing;
    legR.hip.rotation.x = sitFactor * (Math.PI / 2) - swing;
    legL.knee.rotation.x = -sitFactor * (Math.PI / 2) - Math.max(0, -swing) * 0.55;
    legR.knee.rotation.x = -sitFactor * (Math.PI / 2) - Math.max(0, swing) * 0.55;

    // 3. Xương tay: gõ phím / đi bộ vung tay / nói chuyện khua tay / giơ tay xin duyệt
    const [L, R] = this.arms;
    const typing = p.type * 0.08;
    const talkWaveL = p.talk * (0.35 + Math.sin(t * 7 + ph) * 0.22);
    const talkWaveR = p.talk * (0.42 + Math.cos(t * 6.2 + ph) * 0.25);
    const walkArm = Math.sin(this.walkCycle) * 0.45 * p.walk;

    L.rotation.x = -0.32 * p.lap + Math.sin(t * 17 + ph) * typing + talkWaveL - walkArm;
    R.rotation.x = -0.32 * p.lap + Math.sin(t * 15 + ph + 1.7) * typing + p.raise * 2.75 + talkWaveR + walkArm;
    R.rotation.z = -p.raise * (0.25 + Math.sin(t * 6) * 0.22) - p.talk * Math.sin(t * 4.5) * 0.14;
    L.rotation.z = p.talk * Math.cos(t * 4.2) * 0.14;

    // 4. Đầu: gật gù trao đổi khi nói chuyện, gật nhẹ khi gõ, nhìn quanh khi rảnh
    const idleLook = (1 - p.type) * (1 - p.raise) * (1 - p.down) * (1 - p.walk);
    this.headPivot.rotation.y = Math.sin(t * (this.talking ? 2.4 : 0.35) + ph) * (this.talking ? 0.22 : 0.45) * idleLook;
    this.headPivot.rotation.x = Math.sin(t * 2.2 + ph) * 0.03 * p.type + Math.sin(t * 6.5 + ph) * 0.09 * p.talk - 0.5 * p.down + p.raise * 0.12;
    this.body.scale.y = 1 + Math.sin(t * 1.6 + ph) * 0.008;
    if (!this.trip) {
      const base = this.standing > 0.5 ? 0.68 : (this.baseY ?? 0.5);
      this.root.position.y = base + Math.abs(Math.sin(t * 4 + ph)) * 0.03 * p.raise;
    }
  }

  place(x, y, z, facing) {
    this.baseY = y;
    this.root.position.set(x, y, z);
    this.anchor.set(x, 0, z);
    this.root.rotation.y = facing;
  }

  dispose() {
    this.root.traverse(o => o.geometry?.dispose());
    this.mat.dispose();
  }
}
