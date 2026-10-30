// Cảnh văn phòng 3D: vỏ toà nhà, bố cục phòng ban, nhân viên, đèn, hậu kỳ, chọn đối tượng
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { GTAOPass } from 'three/addons/postprocessing/GTAOPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';

import { MAT, PALETTE, blobShadow, poolMaterial, rugMaterial } from './materials.js';
import { floorTiles, skylinePanorama, floorLabel, pillLabel, agentOverheadTag, speechBubbleTag, ScreenBank } from './textures.js';
import { rbox, mesh, rng, mergeStatic, disposeTree, roundedRectShape, markDynamic } from './util.js';
import * as F from './furniture.js';
import { Person } from './people.js';
import { MixamoLibrary } from './mixamo.js';
import { Assets } from './assets.js';
import { NavGrid } from './nav.js';
import * as L from './leisure.js';

const FLOOR = { w: 36, d: 28 };
const TERRACE = 2.6;
const STATUS_RING = { working: '#ffd38a', waiting: '#ff9a4d', queued: '#8fb3ff', error: '#ff6b6b' };
const MAX_POINT_LIGHTS = 8;

/** Hướng nhìn: người dựng quay về -z; trả yaw để nhìn từ (fx,fz) về (tx,tz) */
const faceToward = (fx, fz, tx, tz) => Math.atan2(-(tx - fx), -(tz - fz));
/** Điểm cách chỗ ngồi `dist` mét về phía sau (dist < 0: phía trước) — nơi đứng dậy / bắt đầu đi */
const behind = (x, z, facing, dist) => ({ x: x + Math.sin(facing) * dist, z: z + Math.cos(facing) * dist });
const rand = (a, b) => a + Math.random() * (b - a);
const at = (obj, x, z) => { obj.position.set(x, 0, z); return obj; };
// Thời gian nghỉ (giây): ngồi rảnh bao lâu thì đi, ở lại bao lâu
const BREAK = { first: [6, 40], again: [45, 150], stay: [45, 120] };

/** GTAO bỏ qua sprite, kính, vũng sáng (tránh quầng tối giả) */
class OfficeGTAO extends GTAOPass {
  overrideVisibility() {
    const cache = this._visibilityCache;
    this.scene.traverse(o => {
      cache.set(o, o.visible);
      if (o.isPoints || o.isLine || o.isSprite || o.userData.noAO || (o.material && !Array.isArray(o.material) && o.material.transparent)) o.visible = false;
    });
  }
}

export const QUALITY = { high: 'Cao', medium: 'Vừa', low: 'Thấp' };

export class Office3D {
  constructor(container, { onPick, onHover, onProgress } = {}) {
    this.container = container;
    this.onPick = onPick; this.onHover = onHover; this.onProgress = onProgress;
    this.agents = new Map();     // agentId → visual
    this.clusters = [];          // nhóm bàn có đèn thả
    this.hitboxes = [];
    this.couriers = [];
    this.selectedId = null; this.hoveredId = null;
    this.screens = new ScreenBank();
    this.assets = new Assets();
    this.people = new MixamoLibrary();
    this.mobile = matchMedia('(max-width: 760px)').matches;
    this.quality = this.loadQuality();
    this.layoutSig = '';
    this.spots = [];             // chỗ ngồi ở khu cà phê / giải trí
    this.games = new L.GameScreens();
    this.leisureSpeed = 1;       // >1 để thử nhanh (?nghi=nhanh)
  }

  // ================================================================ khởi tạo
  async init() {
    const r = this.renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
    r.info.autoReset = false;  // đếm draw call cả khung hình (nhiều pass)
    r.toneMapping = THREE.ACESFilmicToneMapping;
    r.toneMappingExposure = 1.15;
    r.outputColorSpace = THREE.SRGBColorSpace;
    r.shadowMap.type = THREE.PCFSoftShadowMap;
    this.container.prepend(r.domElement);

    const scene = this.scene = new THREE.Scene();
    scene.background = new THREE.Color('#05070d');
    const pmrem = new THREE.PMREMGenerator(r);
    scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
    scene.environmentIntensity = 0.22;

    this.camera = new THREE.PerspectiveCamera(37, 1, 0.5, 400);
    this.controls = new OrbitControls(this.camera, r.domElement);
    this.controls.enableDamping = true;
    this.controls.maxPolarAngle = Math.PI * 0.44;
    this.controls.minDistance = 5; this.controls.maxDistance = 70;
    this.home = { pos: new THREE.Vector3(0, 23.5, 28.5), target: new THREE.Vector3(0, 0, 2.2) };   // nhìn trọn cả khu cà phê / giải trí ở mặt tiền

    this.buildLights();
    this.onProgress?.('Đang dựng toà nhà…');
    await this.assets.load(this.onProgress);
    await this.people.load(this.onProgress);   // nhân vật Mixamo (nếu có)
    this.buildShell();

    this.layout = new THREE.Group(); this.layout.name = 'layout';
    this.dynamic = new THREE.Group(); this.dynamic.name = 'dynamic';
    scene.add(this.layout, this.dynamic);

    this.raycaster = new THREE.Raycaster();
    this.pointer = new THREE.Vector2();
    this.bindEvents();
    this.applyQuality(this.quality, false);
    this.resize(true);
    addEventListener('resize', () => this.resize());

    this.clock = new THREE.Clock();
    this.fps = { frames: 0, acc: 0, lastDowngrade: 0 };
    r.setAnimationLoop(() => this.frame());
  }

  loadQuality() {
    try { const q = localStorage.getItem('office.quality'); if (q && QUALITY[q]) return q; } catch { /* chế độ riêng tư */ }
    return this.mobile ? 'low' : 'high';
  }

  buildLights() {
    const s = this.scene;
    s.add(new THREE.HemisphereLight('#727790', '#2e2116', 0.75));
    const moon = this.moon = new THREE.DirectionalLight('#8ea4d6', 0.75);
    moon.position.set(-8, 30, -14);
    moon.castShadow = true;
    Object.assign(moon.shadow.camera, { left: -22, right: 22, top: 20, bottom: -20, near: 1, far: 80 });
    moon.shadow.bias = -0.0004; moon.shadow.normalBias = 0.03;
    s.add(moon, moon.target);
    const warm = new THREE.DirectionalLight('#ffcf9e', 0.6);
    warm.position.set(10, 14, 18);
    s.add(warm);
    // bể đèn điểm thật, gán cho các cụm bàn bận nhất
    this.pointLights = Array.from({ length: MAX_POINT_LIGHTS }, () => {
      const l = new THREE.PointLight(PALETTE.lampWarm, 0, 7, 2);
      l.userData.target = 0;
      s.add(l);
      return l;
    });
  }

  // ================================================================ vỏ toà nhà (dựng một lần)
  buildShell() {
    const shell = new THREE.Group();
    const { w, d } = FLOOR;
    // sàn chính + sàn hiên phía trước
    const floorMat = new THREE.MeshStandardMaterial({ map: floorTiles(w, d), roughness: 0.42, metalness: 0.05 });
    floorMat.userData.shared = true;
    shell.add(mesh(new THREE.PlaneGeometry(w, d), floorMat, 0, 0, 0, { rx: -Math.PI / 2, cast: false }));
    const terraceMat = new THREE.MeshStandardMaterial({ map: floorTiles(w, TERRACE), color: '#8a8d93', roughness: 0.6 });
    terraceMat.userData.shared = true;
    shell.add(mesh(new THREE.PlaneGeometry(w + 1, TERRACE), terraceMat, 0, -0.02, d / 2 + TERRACE / 2, { rx: -Math.PI / 2, cast: false }));
    shell.add(mesh(new THREE.BoxGeometry(w + 1.4, 0.9, d + TERRACE + 0.8), MAT.slab, 0, -0.47, TERRACE / 2, { cast: false }));

    // tường kính phía sau: kính + khung mullion
    const H = 4.4;
    shell.add(mesh(new THREE.PlaneGeometry(w, H), MAT.glass, 0, H / 2, -d / 2, { cast: false, receive: false }));
    for (let x = -w / 2; x <= w / 2 + 0.01; x += 2.4) shell.add(mesh(new THREE.BoxGeometry(0.07, H, 0.1), MAT.frame, x, H / 2, -d / 2, { cast: false }));
    for (const y of [0.05, H]) shell.add(mesh(new THREE.BoxGeometry(w, 0.1, 0.14), MAT.frame, 0, y, -d / 2, { cast: false }));

    // tường bên: đặc ở hai đầu, kính ở đoạn có phòng họp (nhìn ra phố)
    for (const sx of [-1, 1]) {
      const x = sx * w / 2;
      for (const [z0, z1] of [[-d / 2, -4.2], [3.0, d / 2]]) {
        const len = z1 - z0;
        shell.add(mesh(new THREE.BoxGeometry(0.3, 3.4, len), MAT.wall, x + sx * 0.15, 1.7, (z0 + z1) / 2));
        shell.add(mesh(new THREE.BoxGeometry(0.06, 0.12, len), MAT.wood, x - sx * 0.02, 0.06, (z0 + z1) / 2, { cast: false })); // len chân tường
      }
      shell.add(mesh(new THREE.PlaneGeometry(7.2, H), MAT.glass, x, H / 2, -0.6, { ry: Math.PI / 2, cast: false, receive: false }));
      for (let z = -4.2; z <= 3.01; z += 2.4) shell.add(mesh(new THREE.BoxGeometry(0.1, H, 0.07), MAT.frame, x, H / 2, z, { cast: false }));
    }

    // mặt tiền: tường thấp + cửa kính đôi + thảm chùi chân + bồn cây trên hiên
    const fz = d / 2;
    for (const sx of [-1, 1]) shell.add(mesh(rbox(w / 2 - 1.7, 1.0, 0.28, 0.03), MAT.wall, sx * (w / 4 + 0.85), 0.5, fz));
    const door = F.glassDoubleDoor(3.2, 2.7); door.position.set(0, 0, fz); shell.add(door);
    shell.add(mesh(rbox(2.4, 0.02, 1.4, 0.01), MAT.doormat, 0, 0.0, fz + 1.05, { cast: false }));
    for (const sx of [-1, 1]) {
      const pb = F.planterBox(w / 2 - 3.2, 300 + sx);
      pb.position.set(sx * (w / 4 + 1.5), -0.02, fz + 1.7);
      shell.add(pb);
      const big = this.make('plant_big', () => F.bigPlant(410 + sx, 1.05));
      big.position.set(sx * 2.4, -0.02, fz + 1.1); shell.add(big);
    }

    // skyline đêm quấn quanh toà nhà
    const sky = new THREE.Mesh(
      new THREE.CylinderGeometry(78, 78, 110, 64, 1, true),
      new THREE.MeshBasicMaterial({ map: skylinePanorama(), side: THREE.BackSide, fog: false, toneMapped: false, color: '#c9c9c9' }));
    sky.position.y = -38;
    sky.userData.noAO = true; sky.userData.dynamic = true;
    shell.add(sky);
    const ground = new THREE.Mesh(new THREE.CircleGeometry(78, 48).rotateX(-Math.PI / 2), new THREE.MeshBasicMaterial({ color: '#070a12', fog: false }));
    ground.position.y = -92; ground.userData.dynamic = true; shell.add(ground);

    const merged = mergeStatic(shell);
    this.scene.add(merged);
    // phần động (skyline) giữ nguyên
    shell.children.slice().forEach(c => c.userData.dynamic && this.scene.add(c));
  }

  /** Model GLB thay thế nếu có trong manifest, không thì dùng bản dựng bằng code */
  make(key, fallback) {
    return this.assets.instance(key) ?? fallback();
  }

  // ================================================================ dữ liệu → cảnh
  setData(departments, agents) {
    this.lastData = [departments, agents];
    const sig = JSON.stringify(departments) + '|' + agents.map(a => `${a.id}:${a.departmentId}:${a.name}:${a.provider}`).join(',') + '|' + this.quality;
    if (sig !== this.layoutSig) {
      this.rebuild(departments, agents);
      this.layoutSig = sig;            // chỉ ghi nhận khi dựng thành công
    }
    for (const a of agents) {
      this.setStatus(a.id, a.status, true);
      this.setAgentProgress(a.id, { pct: a.progressPct, activityText: a.activityText, queued: a.queued, status: a.status });
    }
    this.refreshLights();
  }

  rebuild(departments, agents) {
    // dọn bản cũ
    for (const v of this.agents.values()) v.person.dispose();
    disposeTree(this.layout); disposeTree(this.dynamic);
    this.scene.remove(this.layout, this.dynamic);
    this.layout = new THREE.Group(); this.dynamic = new THREE.Group();
    this.scene.add(this.layout, this.dynamic);
    this.agents.clear(); this.clusters = []; this.hitboxes = [];
    this.games.dispose(); this.spots = [];
    this.nav = new NavGrid(FLOOR.w, FLOOR.d);

    const build = new THREE.Group();           // gom tĩnh rồi gộp
    const dense = this.dense = this.quality !== 'low';
    const byDept = new Map(departments.map(d => [d.id, []]));
    for (const a of agents) (byDept.get(a.departmentId) ?? byDept.set(a.departmentId, []).get(a.departmentId)).push(a);

    for (const d of departments) {
      const style = { shape: 'zone', screenTheme: 'docs', ...(d.style || {}) };
      const members = byDept.get(d.id) ?? [];
      if (style.shape === 'lounge') this.buildLounge(d, style, members, build);
      else if (style.shape === 'room') this.buildRoom(d, style, members, build);
      else if (style.shape === 'cafe' && !members.length) this.buildCafe(d, style, build);
      else if (style.shape === 'game' && !members.length) this.buildGame(d, style, build);   // lỡ xếp người vào khu nghỉ → dựng bàn làm việc để không ai bị mất
      else this.buildZone(d, style, members, build);
    }
    this.buildDecor(departments, build, dense);
    this.layout.add(mergeStatic(build));
    // phần động còn lại trong build (đèn, vũng sáng…) chuyển sang nhóm dynamic
    const leftovers = [];
    build.traverse(o => { if (o !== build && o.userData.dynamic && !o.parent?.userData.dynamic) leftovers.push(o); });
    for (const o of leftovers) { o.updateMatrixWorld(true); const m = o.matrixWorld.clone(); o.parent.remove(o); m.decompose(o.position, o.quaternion, o.scale); this.dynamic.add(o); }
    this.applyShadows();
  }

  // ---------------------------------------------------------------- thảm phòng ban + nhãn
  addRug(d, build, wobble, seedR) {
    const shape = roundedRectShape(d.w, d.d, Math.min(2.2, Math.min(d.w, d.d) * 0.3), wobble, seedR);
    const geo = new THREE.ExtrudeGeometry(shape, { depth: 0.02, bevelEnabled: true, bevelSize: 0.03, bevelThickness: 0.01, bevelSegments: 2, curveSegments: 18 });
    geo.rotateX(-Math.PI / 2);
    build.add(mesh(geo, rugMaterial(d.color), d.x, 0.0, d.z, { cast: false }));
  }
  addLabel(text, x, z, maxW, build, h = 0.42) {
    const { texture, aspect } = floorLabel(text);
    const w = Math.min(maxW, h * aspect), hh = w / aspect;
    const m = new THREE.Mesh(new THREE.PlaneGeometry(w, hh), new THREE.MeshBasicMaterial({ map: texture, transparent: true, depthWrite: false, toneMapped: false, color: '#ffffff', polygonOffset: true, polygonOffsetFactor: -3 }));
    m.rotation.x = -Math.PI / 2; m.position.set(x, 0.045, z); m.renderOrder = 2;
    markDynamic(m);
    build.add(m);
  }

  // ---------------------------------------------------------------- khu cụm bàn
  buildZone(d, style, members, build) {
    const r = rng(style.seed ?? 1);
    // chia người vào cụm bench: 3–4 cột × 2 hàng (tối đa 8 chỗ một cụm)
    const groups = [];
    for (let i = 0; i < Math.max(1, members.length); i += 8) groups.push(members.slice(i, i + 8));
    const clusterDepth = 3.0, gap = 0.55;
    const needD = groups.length * clusterDepth + (groups.length - 1) * gap + 1.4;
    const zone = { ...d, d: Math.max(d.d, needD) };
    this.addRug(zone, build, 0.22, r);
    this.addLabel(style.label || d.name, zone.x, zone.z + zone.d / 2 - 0.55, zone.w * 0.62, build, 0.62);

    const top = zone.z - (groups.length * clusterDepth + (groups.length - 1) * gap) / 2 + clusterDepth / 2 - 0.25;
    groups.forEach((g, gi) => {
      const cols = Math.min(4, Math.max(3, Math.ceil(g.length / 2)));
      const cx = zone.x + (r() - 0.5) * 0.4, cz = top + gi * (clusterDepth + gap);
      const desk = F.benchDesk(cols); desk.position.set(cx, 0, cz); build.add(desk);
      const deskW = cols * F.SEAT_PITCH + 0.2;
      this.nav.rect(cx - deskW / 2, cz - F.DESK_DEPTH / 2, cx + deskW / 2, cz + F.DESK_DEPTH / 2);
      const cluster = { id: `${d.id}-${gi}`, deptId: d.id, agents: [], lamps: [], center: new THREE.Vector3(cx, 2.2, cz) };
      // thứ tự chỗ: xen kẽ hàng trước (phía camera) / hàng sau, cột từ giữa ra
      const slots = [];
      const colOrder = [...Array(cols).keys()].sort((a, b) => Math.abs(a - (cols - 1) / 2) - Math.abs(b - (cols - 1) / 2));
      for (const c of colOrder) for (const row of [1, -1]) slots.push({ c, row });
      for (let i = 0; i < cols * 2; i++) {
        const { c, row } = slots[i];
        const agent = g[i];
        const x = cx + (c - (cols - 1) / 2) * F.SEAT_PITCH;
        const yaw = row === 1 ? 0 : Math.PI;           // hàng trước quay về -z
        const ws = F.workstation({ device: agent?.provider === 'codex' ? 'laptop' : 'imac', seed: (style.seed ?? 1) * 31 + i, decor: this.dense });
        ws.group.position.set(x, 0, cz + row * 0.38);
        ws.group.rotation.y = yaw;
        build.add(ws.group);
        const chair = this.make('chair_office', () => F.officeChair(i + gi));
        const cz2 = cz + row * 1.12;
        chair.position.set(x, 0, cz2); chair.rotation.y = yaw + (r() - 0.5) * 0.25;
        build.add(chair);
        this.nav.circle(x, cz2, 0.26);
        ws.screen.material = this.screens.material(style.screenTheme, agent ? agent.status : 'offline');
        if (agent) {
          const sx = x, sz = cz + row * 1.02;
          this.addAgent(agent, { x: sx, y: 0.5, z: sz, facing: yaw, screen: ws.screen, theme: style.screenTheme, cluster, deptColor: d.color, focus: new THREE.Vector3(x, 1.2, cz + row * 0.6) });
        }
      }
      // đồ trên vách giữa bàn
      for (let c = 0; c < cols; c += 2) {
        const p = F.deskPlant(gi * 13 + c + (style.seed ?? 0), 1.3);
        p.position.set(cx + (c - (cols - 1) / 2) * F.SEAT_PITCH + 0.7, F.DESK_TOP, cz);
        build.add(p);
      }
      // đèn thả: mỗi cột 1 chiếc
      for (let c = 0; c < cols; c++) this.addPendant(cluster, cx + (c - (cols - 1) / 2) * F.SEAT_PITCH, cz, build, F.DESK_TOP);
      this.clusters.push(cluster);
    });
    // cây góc thảm
    if (this.dense) {
      for (const [sx, sz] of [[-1, -1], [1, 1]]) {
        const p = this.make('plant_big', () => F.bigPlant((style.seed ?? 1) * 5 + sx * 3 + sz, 0.9));
        p.position.set(zone.x + sx * (zone.w / 2 - 0.7), 0, zone.z + sz * (zone.d / 2 - 0.75));
        build.add(p);
        this.nav.circle(p.position.x, p.position.z, 0.32);
      }
    }
  }

  addPendant(cluster, x, z, build, surfaceY) {
    const { group, bulb } = F.pendantLamp(2.5);
    group.position.set(x, 0, z);
    build.add(group);
    const pool = new THREE.Mesh(new THREE.PlaneGeometry(1, 1).rotateX(-Math.PI / 2), cluster.poolMat ??= poolMaterial(PALETTE.lampWarm, 0.2));
    pool.scale.set(2.0, 1, 1.6);
    pool.position.set(x, surfaceY + 0.006, z);
    pool.renderOrder = 3; pool.userData.noAO = true;
    markDynamic(pool);
    build.add(pool);
    cluster.lamps.push({ bulb, pos: new THREE.Vector3(x, 2.35, z) });
  }

  // ---------------------------------------------------------------- lounge điều phối
  buildLounge(d, style, members, build) {
    const R = Math.min(d.w, d.d) / 2;
    build.add(mesh(new THREE.CircleGeometry(R, 72).rotateX(-Math.PI / 2), MAT.rugLounge, d.x, 0.008, d.z, { cast: false }));
    build.add(mesh(new THREE.RingGeometry(R - 0.32, R - 0.26, 72).rotateX(-Math.PI / 2), rugMaterial('#3a3b3f'), d.x, 0.01, d.z, { cast: false }));
    this.addLabel(style.label || d.name, d.x, d.z + R - 0.55, R * 1.1, build, 0.36);

    const center = new THREE.Vector3(d.x, 0, d.z);
    const sofa = F.curvedSofa(2.15, 2.4); sofa.group.position.copy(center); build.add(sofa.group);
    const table = this.make('coffee_table', () => F.coffeeTable(0.8, style.seed ?? 1)); table.position.copy(center); build.add(table);
    for (let a = Math.PI / 2 - 1.2; a <= Math.PI / 2 + 1.21; a += 0.2) this.nav.circle(d.x + Math.cos(a) * 2.2, d.z - Math.sin(a) * 2.2, 0.3);
    this.nav.circle(d.x, d.z, 0.72);
    const cluster = { id: d.id, deptId: d.id, agents: [], lamps: [], center: new THREE.Vector3(d.x, 2.2, d.z) };
    this.addPendant(cluster, d.x, d.z, build, 0.47);

    // chỗ ngồi: 2 ghế bành phía trước, 3 chỗ sofa, đôn, rồi ghế phụ quanh vòng
    const seats = [];
    for (const sgn of [-1, 1]) {
      const a = -Math.PI / 2 + sgn * 0.95, rr = 1.85;
      const x = d.x + Math.cos(a) * rr, z = d.z - Math.sin(a) * rr;
      const facing = faceToward(x, z, d.x, d.z);
      const ch = this.make('armchair', () => F.armchair());
      ch.position.set(x, 0, z); ch.rotation.y = facing + Math.PI;
      build.add(ch);
      this.nav.circle(x, z, 0.36);
      seats.push({ x, z, facing, seatH: 0.5, exit: behind(x, z, facing, 0.85) });
    }
    seats.push(sofa.seats[1], sofa.seats[0], sofa.seats[2]);
    for (const s of seats.slice(2)) { s.x += d.x; s.z += d.z; s.exit = behind(s.x, s.z, s.facing, -0.62); }   // sofa: đứng dậy bước về phía trước
    const ott = F.ottoman(style.seed ?? 3); ott.position.set(d.x, 0, d.z + 1.55); build.add(ott);
    this.nav.circle(d.x, d.z + 1.55, 0.32);
    const of = faceToward(d.x, d.z + 1.55, d.x, d.z);
    seats.push({ x: d.x, z: d.z + 1.55, facing: of, seatH: 0.44, exit: behind(d.x, d.z + 1.55, of, 0.75) });
    for (let i = seats.length; i < members.length; i++) {
      const a = -Math.PI / 2 + (i - seats.length + 1) * 0.55 * ((i % 2) ? 1 : -1) + Math.PI * 0.62 * ((i % 2) ? 1 : -1);
      const rr = 2.7, x = d.x + Math.cos(a) * rr, z = d.z - Math.sin(a) * rr;
      const ot = F.ottoman(i); ot.position.set(x, 0, z); build.add(ot);
      this.nav.circle(x, z, 0.32);
      const f = faceToward(x, z, d.x, d.z);
      seats.push({ x, z, facing: f, seatH: 0.44, exit: behind(x, z, f, 0.75) });
    }
    members.forEach((a, i) => {
      const s = seats[i];
      const lap = F.laptop();
      this.addAgent(a, {
        x: s.x, y: s.seatH, z: s.z, facing: s.facing, screen: lap.screen, theme: style.screenTheme, cluster,
        focus: new THREE.Vector3(s.x, 1.1, s.z), lapDevice: lap.group, variant: 'lounge', exit: s.exit, deptColor: d.color,
      });
    });
    if (members.length === 0) { const lap = F.laptop(); lap.group.position.set(d.x - 0.2, 0.47, d.z + 0.2); lap.group.rotation.y = 0.4; lap.screen.material = this.screens.material(style.screenTheme, 'idle'); build.add(lap.group); }
    // cây lớn hai bên sofa
    const pl = this.make('plant_big', () => F.monstera((style.seed ?? 1) + 2, 1.15)); pl.position.set(d.x + 2.75, 0, d.z - 1.35); build.add(pl);
    const pr = this.make('plant_big', () => F.fiddleFig((style.seed ?? 1) + 5, 1.05)); pr.position.set(d.x - 2.85, 0, d.z - 1.25); build.add(pr);
    this.nav.circle(d.x + 2.75, d.z - 1.35, 0.38); this.nav.circle(d.x - 2.85, d.z - 1.25, 0.38);
    this.clusters.push(cluster);
  }

  // ---------------------------------------------------------------- phòng họp kính
  buildRoom(d, style, members, build) {
    const side = Math.sign(d.x) || 1;                // phòng nằm sát tường trái (-) hoặc phải (+)
    const innerX = d.x - side * d.w / 2;
    const H = 2.7;
    build.add(mesh(rbox(d.w - 0.1, 0.02, d.d - 0.1, 0.01), rugMaterial(d.color), d.x, 0.006, d.z, { cast: false }));
    // vách kính phía trong (có cửa ở giữa) + vách trước/sau
    const doorW = 1.1, seg = (d.d - doorW) / 2;
    for (const sz of [-1, 1]) {
      const z = d.z + sz * (doorW / 2 + seg / 2);
      build.add(mesh(new THREE.PlaneGeometry(seg, H), MAT.glassRoom, innerX, H / 2, z, { ry: Math.PI / 2, cast: false, receive: false }));
    }
    for (const sz of [-1, 1]) build.add(mesh(new THREE.PlaneGeometry(d.w, H), MAT.glassRoom, d.x, H / 2, d.z + sz * d.d / 2, { cast: false, receive: false }));
    const post = (x, z) => build.add(mesh(new THREE.BoxGeometry(0.06, H, 0.06), MAT.frame, x, H / 2, z, { cast: false }));
    for (const sz of [-1, 1]) { post(innerX, d.z + sz * d.d / 2); post(innerX, d.z + sz * doorW / 2); }
    build.add(mesh(new THREE.BoxGeometry(0.07, 0.07, d.d), MAT.frame, innerX, H, d.z, { cast: false }));
    for (const sz of [-1, 1]) build.add(mesh(new THREE.BoxGeometry(d.w, 0.07, 0.07), MAT.frame, d.x, H, d.z + sz * d.d / 2, { cast: false }));
    // cánh cửa kính hé mở
    const leaf = mesh(new THREE.PlaneGeometry(doorW - 0.05, H - 0.1), MAT.glassRoom, innerX + side * 0.38, (H - 0.1) / 2, d.z - doorW / 2 + 0.38, { ry: Math.PI / 2 - side * 0.9, cast: false, receive: false });
    build.add(leaf);
    // vách kính chặn đường đi, chừa lối cửa
    for (const sz of [-1, 1]) {
      this.nav.wall(innerX, d.z + sz * (doorW / 2 + 0.05), innerX, d.z + sz * d.d / 2);
      this.nav.wall(innerX, d.z + sz * d.d / 2, d.x + side * d.w / 2, d.z + sz * d.d / 2);
    }

    // bàn tròn + ghế
    const tx = d.x + side * 0.15, tz = d.z;
    build.add(mesh(new THREE.CylinderGeometry(0.55, 0.55, 0.04, 32), MAT.desk, tx, 0.74, tz));
    build.add(mesh(new THREE.CylinderGeometry(0.05, 0.22, 0.72, 16), MAT.aluminium, tx, 0.36, tz));
    build.add(blobShadow(1.6, 1.6).translateX(tx).translateZ(tz));
    this.nav.circle(tx, tz, 0.55);
    const cluster = { id: d.id, deptId: d.id, agents: [], lamps: [], center: new THREE.Vector3(tx, 2.2, tz) };
    this.addPendant(cluster, tx, tz, build, 0.76);
    const angles = [Math.PI, 0, Math.PI / 2, -Math.PI / 2];
    const n = Math.max(members.length, 3);
    for (let i = 0; i < Math.min(n, 4); i++) {
      const a = angles[i];
      const x = tx + Math.sin(a) * 0.95, z = tz + Math.cos(a) * 0.95;
      const facing = faceToward(x, z, tx, tz);
      const ch = this.make('chair_office', () => F.officeChair(i * 7)); ch.position.set(x, 0, z); ch.rotation.y = facing; build.add(ch);
      this.nav.circle(x, z, 0.24);
      const agent = members[i];
      const lap = F.laptop();
      lap.group.position.set(tx + Math.sin(a) * 0.32, 0.76, tz + Math.cos(a) * 0.32);
      lap.group.rotation.y = facing;
      build.add(lap.group);
      lap.screen.material = this.screens.material(style.screenTheme, agent ? agent.status : 'offline');
      if (agent) this.addAgent(agent, { x: tx + Math.sin(a) * 0.86, y: 0.5, z: tz + Math.cos(a) * 0.86, facing, screen: lap.screen, theme: style.screenTheme, cluster, focus: new THREE.Vector3(x, 1.2, z), exit: behind(x, z, facing, 0.7) });
    }
    // người thứ 5 trở đi: ghế dọc vách
    members.slice(4).forEach((agent, k) => {
      const x = d.x - side * 0.2, z = d.z - d.d / 2 + 0.7 + k * 0.9;
      const facing = faceToward(x, z, tx, tz);
      const ch = F.officeChair(k); ch.position.set(x, 0, z); ch.rotation.y = facing; build.add(ch);
      this.nav.circle(x, z, 0.24);
      const lap = F.laptop();
      this.addAgent(agent, { x, y: 0.5, z, facing, screen: lap.screen, theme: style.screenTheme, cluster, focus: new THREE.Vector3(x, 1.2, z), lapDevice: lap.group });
    });
    // trang trí: đèn sàn góc, tranh tường ngoài, cây
    const fl = this.make('floor_lamp', () => F.floorLamp()); fl.position.set(d.x + side * (d.w / 2 - 0.4), 0, d.z - d.d / 2 + 0.45); build.add(fl);
    const plant = this.make('plant_big', () => F.snakePlant((style.seed ?? 1) + 9, 1.1)); plant.position.set(d.x + side * (d.w / 2 - 0.4), 0, d.z + d.d / 2 - 0.45); build.add(plant);
    this.nav.circle(fl.position.x, fl.position.z, 0.2); this.nav.circle(plant.position.x, plant.position.z, 0.25);
    this.addLabel(style.label || d.name, d.x - side * 0.25, d.z + d.d / 2 - 0.42, d.w * 0.75, build, 0.3);
    this.clusters.push(cluster);
  }

  // ---------------------------------------------------------------- khu cà phê
  /** Quầy bar + ghế cao + 2 bàn tròn. Nhân viên rảnh ra đây ngồi uống cà phê, nói chuyện */
  buildCafe(d, style, build) {
    const r = rng(style.seed ?? 7);
    const W = (lx, lz) => [d.x + lx, d.z + lz];
    this.addRug(d, build, 0.16, r);
    this.addLabel(style.label || d.name, d.x + 1.6, d.z + d.d / 2 - 0.45, d.w * 0.4, build, 0.5);
    const cluster = { id: d.id, deptId: d.id, agents: [], lamps: [], center: new THREE.Vector3(d.x - 1, 2.2, d.z), amenity: true, occupants: new Set() };
    const spot = (o) => this.spots.push({ kind: 'cafe', variant: 'cafe', prop: 'cup', cluster, occupant: null, ...o });

    // quầy bar + kệ sau quầy + biển neon
    const barX = -d.w / 2 + 2.35, barLen = 3.6;
    const [bx, bz] = W(barX, -0.72);
    const bar = L.coffeeBar(barLen, style.seed ?? 7); bar.position.set(bx, 0, bz); build.add(bar);
    this.nav.rect(bx - barLen / 2 - 0.05, bz - 0.34, bx + barLen / 2 + 0.05, bz + 0.34);
    const [kx, kz] = W(barX, -1.72);
    const back = L.backBar(barLen - 0.2); back.position.set(kx, 0, kz); build.add(back);
    this.nav.rect(kx - barLen / 2, kz - 0.22, kx + barLen / 2, kz + 0.22);
    const sign = L.neonSign(style.sign || 'CÀ PHÊ', '#ffb46b', 2.0); sign.position.set(kx, 2.62, kz + 0.05); build.add(sign);
    for (const lx of [barX - 0.95, barX + 0.95]) { const [px, pz] = W(lx, -0.72); this.addPendant(cluster, px, pz, build, 1.08); }
    // ghế cao trước quầy (người ngồi quay vào quầy, -z)
    [-1.1, 0, 1.1].forEach((off, i) => {
      const [sx, sz] = W(barX + off, 0.0);
      build.add(at(L.barStool(i + 1), sx, sz));
      this.nav.circle(sx, sz, 0.2);
      spot({ id: `${d.id}-bar-${i}`, group: `${d.id}-bar`, x: sx, z: sz, facing: 0, seatH: 0.74, exit: behind(sx, sz, 0, 0.75) });
    });
    // 2 bàn tròn, mỗi bàn 3 ghế (trái, phải, phía sau quay mặt ra ngoài)
    [[0.7, 0.3], [3.45, 0.05]].forEach(([lx, lz], ti) => {
      const [tx, tz] = W(lx, lz);
      build.add(at(L.bistroTable((style.seed ?? 7) * 3 + ti), tx, tz));
      this.nav.circle(tx, tz, 0.4);
      this.addPendant(cluster, tx, tz, build, 0.76);
      [[-0.66, 0], [0.66, 0], [0, -0.66]].forEach(([ox, oz], ci) => {
        const cx = tx + ox, cz = tz + oz, facing = faceToward(cx, cz, tx, tz);
        const ch = L.bistroChair(); ch.position.set(cx, 0, cz); ch.rotation.y = facing; build.add(ch);
        this.nav.circle(cx, cz, 0.24);
        spot({ id: `${d.id}-t${ti}-${ci}`, group: `${d.id}-t${ti}`, x: cx, z: cz, facing, seatH: 0.5, exit: behind(cx, cz, facing, 0.7) });
      });
    });
    // bảng menu, cây
    const [mx, mz] = W(d.w / 2 - 0.75, 1.15);
    const menu = L.menuBoard(); menu.position.set(mx, 0, mz); menu.rotation.y = -0.35; build.add(menu);
    this.nav.circle(mx, mz, 0.3);
    for (const [lx, lz, k] of [[-d.w / 2 + 0.55, 1.35, 1], [d.w / 2 - 0.6, -1.45, 2]]) {
      const [px, pz] = W(lx, lz);
      const p = this.make('plant_big', () => F.bigPlant((style.seed ?? 7) * 11 + k, 0.95)); p.position.set(px, 0, pz); build.add(p);
      this.nav.circle(px, pz, 0.34);
    }
    this.clusters.push(cluster);
  }

  // ---------------------------------------------------------------- khu giải trí
  /** TV + sofa chơi game, 2 máy arcade, bàn bi lắc */
  buildGame(d, style, build) {
    const r = rng(style.seed ?? 8);
    const W = (lx, lz) => [d.x + lx, d.z + lz];
    this.addRug(d, build, 0.16, r);
    this.addLabel(style.label || d.name, d.x - 1.4, d.z + d.d / 2 - 0.45, d.w * 0.4, build, 0.5);
    const cluster = { id: d.id, deptId: d.id, agents: [], lamps: [], center: new THREE.Vector3(d.x - 2, 2.2, d.z), amenity: true, occupants: new Set() };
    const spot = (o) => this.spots.push({ kind: 'game', variant: 'game', prop: 'pad', cluster, occupant: null, ...o });

    // TV + sofa
    const tvX = -d.w / 2 + 3.3;
    const [vx, vz] = W(tvX, -1.45);
    const tv = L.tvWall(2.4); tv.group.position.set(vx, 0, vz); build.add(tv.group);
    const tvScreen = this.games.add('tv', tv.screen);
    this.nav.rect(vx - 1.2, vz - 0.25, vx + 1.2, vz + 0.25);
    const sign = L.neonSign(style.sign || 'GAME ZONE', '#ff4fb8', 2.0); sign.position.set(vx, 2.7, vz - 0.12); build.add(sign);
    const [fx, fz] = W(tvX, 0.6);
    const sofa = L.straightSofa(2.3); sofa.group.position.set(fx, 0, fz); build.add(sofa.group);
    this.nav.rect(fx - 1.15, fz - 0.45, fx + 1.15, fz + 0.45);
    sofa.seats.forEach((st, i) => {
      const x = fx + st.x, z = fz + st.z;
      spot({ id: `${d.id}-sofa-${i}`, group: `${d.id}-tv`, screen: tvScreen, x, z, facing: 0, seatH: st.seatH, exit: behind(x, z, 0, -0.7) });
    });
    // 2 ghế bành hai bên, nhìn vào TV
    for (const lx of [tvX - 1.95, tvX + 1.95]) {
      const [ax, az] = W(lx, -0.15);
      const facing = faceToward(ax, az, vx, vz);
      const ch = this.make('armchair', () => F.armchair()); ch.position.set(ax, 0, az); ch.rotation.y = facing + Math.PI; build.add(ch);
      this.nav.circle(ax, az, 0.36);
      spot({ id: `${d.id}-arm-${lx > tvX ? 1 : 0}`, group: `${d.id}-tv`, screen: tvScreen, x: ax, z: az, facing, seatH: 0.5, exit: behind(ax, az, facing, 0.8) });
    }
    this.addPendant(cluster, fx, fz - 0.3, build, 0.5);
    // máy arcade + ghế cao
    [0, 1].forEach(i => {
      const [cx, cz] = W(tvX + 2.95 + i * 0.95, -1.4);
      const cab = L.arcadeCabinet(i); cab.group.position.set(cx, 0, cz); build.add(cab.group);
      const scr = this.games.add('arcade', cab.screen);
      this.nav.rect(cx - 0.4, cz - 0.42, cx + 0.4, cz + 0.42);
      const sx = cx, sz = cz + 0.82;
      build.add(at(L.barStool(i + 4), sx, sz));
      this.nav.circle(sx, sz, 0.2);
      spot({ id: `${d.id}-arcade-${i}`, group: `${d.id}-arcade-${i}`, variant: 'arcade', prop: null, screen: scr, x: sx, z: sz, facing: 0, seatH: 0.74, exit: behind(sx, sz, 0, 0.7) });
    });
    // bàn bi lắc, ghế lười, cây
    const [bx, bz] = W(d.w / 2 - 1.55, 0.25);
    build.add(at(L.foosballTable(), bx, bz));
    this.nav.rect(bx - 0.7, bz - 0.45, bx + 0.7, bz + 0.45);
    this.addPendant(cluster, bx, bz, build, 0.86);
    for (const [lx, lz, m] of [[tvX + 2.6, 1.2, L.LM.sofaPillowB], [tvX + 3.6, 1.35, L.LM.cabinetB]]) {
      const [px, pz] = W(lx, lz);
      const bb = L.beanBag(m); bb.position.set(px, 0, pz); bb.rotation.y = r() * 6; build.add(bb);
      this.nav.circle(px, pz, 0.38);
    }
    for (const [lx, lz, k] of [[d.w / 2 - 0.55, -1.45, 1], [-d.w / 2 + 0.55, 1.35, 2]]) {
      const [px, pz] = W(lx, lz);
      const p = this.make('plant_big', () => F.bigPlant((style.seed ?? 8) * 13 + k, 0.95)); p.position.set(px, 0, pz); build.add(p);
      this.nav.circle(px, pz, 0.34);
    }
    this.clusters.push(cluster);
  }

  // ---------------------------------------------------------------- trang trí chung
  buildDecor(departments, build, dense) {
    const { w, d } = FLOOR;
    const blocked = departments.map(dep => {
      const shape = dep.style?.shape;
      if (shape === 'lounge') return { circle: true, x: dep.x, z: dep.z, r: Math.min(dep.w, dep.d) / 2 + 0.6 };
      return { x0: dep.x - dep.w / 2 - 0.5, x1: dep.x + dep.w / 2 + 0.5, z0: dep.z - dep.d / 2 - 0.5, z1: dep.z + dep.d / 2 + 0.5 };
    });
    const free = (x, z) => !blocked.some(b => b.circle ? Math.hypot(x - b.x, z - b.z) < b.r : x > b.x0 && x < b.x1 && z > b.z0 && z < b.z1)
      && !(Math.abs(x) < 2.2 && z > d / 2 - 3.5);   // lối vào cửa chính
    const r = rng(99);
    // kệ sách + tranh dọc tường bên
    for (const sx of [-1, 1]) {
      for (const z of [-11.4, -9.6, 5.6, 7.4, 9.2]) {
        if (!free(sx * (w / 2 - 0.6), z) && !free(sx * (w / 2 - 0.3), z)) continue;
        const bs = this.make('bookshelf', () => F.bookshelf(1.7, 2.1, Math.round(z * 10) + sx * 3));
        bs.position.set(sx * (w / 2 - 0.2), 0, z); bs.rotation.y = -sx * Math.PI / 2;
        build.add(bs);
        this.nav.orect(bs.position.x, z, 1.7, 0.4, bs.rotation.y);
      }
      const art = F.framedArt(0.9, 1.15, 50 + sx); art.position.set(sx * (w / 2 - 0.02), 2.0, 11.4); art.rotation.y = -sx * Math.PI / 2; build.add(art);
      const art2 = F.framedArt(1.1, 0.8, 60 + sx); art2.position.set(sx * (w / 2 - 0.02), 2.6, -7.0); art2.rotation.y = -sx * Math.PI / 2; build.add(art2);
      const fl = this.make('floor_lamp', () => F.floorLamp()); fl.position.set(sx * (w / 2 - 0.6), 0, 10.6);
      if (free(sx * (w / 2 - 0.6), 10.6)) { build.add(fl); this.nav.circle(fl.position.x, 10.6, 0.2); }
    }
    // cây lớn: dọc kính sau, các góc, mép trước, lối đi giữa
    const spots = [];
    for (let x = -15.6; x <= 15.7; x += dense ? 3.9 : 7.8) spots.push([x + (r() - 0.5) * 1.2, -d / 2 + 0.7 + r() * 0.5]);
    spots.push([-w / 2 + 0.8, d / 2 - 0.8], [w / 2 - 0.8, d / 2 - 0.8], [-4.2, d / 2 - 0.9], [4.2, d / 2 - 0.9], [-w / 2 + 0.8, -3.6], [w / 2 - 0.8, -3.6], [-w / 2 + 0.8, 3.6], [w / 2 - 0.8, 3.6]);
    if (dense) spots.push([0, -10.2], [-14.8, 12.6], [14.8, 12.6]);
    spots.forEach(([x, z], i) => {
      if (!free(x, z)) return;
      const p = this.make('plant_big', () => F.bigPlant(1000 + i * 17, 0.85 + r() * 0.35));
      p.position.set(x, 0, z); p.rotation.y = r() * Math.PI * 2;
      build.add(p);
      this.nav.circle(x, z, 0.32);
    });
  }

  // ---------------------------------------------------------------- nhân viên
  addAgent(agent, { x, y, z, facing, screen, theme, cluster, focus, lapDevice, variant = 'desk', exit, deptColor = '#10b981' }) {
    const person = this.people.create(agent.id) ?? new Person(agent.id);
    person.variant = variant;
    person.place(x, y, z, facing);
    if (lapDevice && person instanceof Person) {
      lapDevice.position.set(0, 0.1, -0.36);
      lapDevice.rotation.set(-0.1, 0, 0);
      person.root.add(lapDevice);
      lapDevice.traverse(o => { o.userData.dynamic = true; o.castShadow = true; });
    }
    this.dynamic.add(person.root);
    markDynamic(screen);

    const ring = new THREE.Mesh(new THREE.RingGeometry(0.46, 0.55, 40).rotateX(-Math.PI / 2),
      new THREE.MeshBasicMaterial({ color: '#ffd38a', transparent: true, opacity: 0.25, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false }));
    ring.position.set(x, 0.03, z); ring.renderOrder = 4; ring.userData.noAO = true;
    this.dynamic.add(ring);

    const tagData = agentOverheadTag(agent.name, {
      status: agent.status ?? 'idle',
      pct: agent.progressPct ?? 0,
      activity: agent.activityText ?? 'Sẵn sàng',
      queued: agent.queued ?? 0,
      isSelected: agent.id === this.selectedId,
      deptColor,
    });
    const label = new THREE.Sprite(new THREE.SpriteMaterial({ map: tagData.texture, transparent: true, depthTest: false }));
    label.scale.set(0.46 * tagData.aspect, 0.46, 1);
    label.userData.aspect = tagData.aspect;
    label.userData.h = 0.46;
    label.position.set(x, 1.92 + y - 0.5, z);
    label.renderOrder = 10;
    label.visible = true; // Luôn hiển thị thẻ tên + trạng thái + % trên đầu
    this.dynamic.add(label);

    // Bong bóng hội thoại khi trao đổi công việc
    const bData = speechBubbleTag('Sẵn sàng', { accent: deptColor });
    const bubble = new THREE.Sprite(new THREE.SpriteMaterial({ map: bData.texture, transparent: true, depthTest: false }));
    bubble.scale.set(0.24 * bData.aspect, 0.24, 1);
    bubble.userData.aspect = bData.aspect;
    bubble.userData.h = 0.24;
    bubble.position.set(x, 2.32 + y - 0.5, z);
    bubble.renderOrder = 12;
    bubble.visible = false;
    this.dynamic.add(bubble);

    const al = pillLabel('!', { size: 56, color: '#1a1205', bg: '#ff9a4d', pad: 12 });
    const alert = new THREE.Sprite(new THREE.SpriteMaterial({ map: al.texture, transparent: true, depthTest: false }));
    alert.scale.set(0.34 * al.aspect, 0.34, 1); alert.userData.aspect = al.aspect; alert.userData.h = 0.34; alert.position.set(x, 2.3 + y - 0.5, z); alert.renderOrder = 11; alert.visible = false;
    this.dynamic.add(alert);

    const hit = new THREE.Mesh(new THREE.BoxGeometry(1.15, 1.8, 1.35), new THREE.MeshBasicMaterial());
    hit.position.set(x, 0.85, z); hit.rotation.y = facing; hit.updateMatrixWorld(true);
    hit.userData.agentId = agent.id;
    this.hitboxes.push(hit);

    cluster.agents.push(agent.id);
    const home = { x, z, facing, seatH: y, variant, prop: null, exit: exit ?? behind(x, z, facing, 0.95) };
    this.agents.set(agent.id, {
      id: agent.id,
      name: agent.name,
      deptColor,
      person,
      screen,
      theme,
      ring,
      label,
      bubble,
      bubbleTimer: 0,
      alert,
      hit,
      cluster,
      focus,
      status: agent.status ?? 'idle',
      progressPct: agent.progressPct ?? 0,
      activityText: agent.activityText ?? 'Sẵn sàng',
      queued: agent.queued ?? 0,
      pos: new THREE.Vector3(x, 1.25, z),
      home,
      where: 'home',
      spot: null,
      breakIn: null,
      stay: 0,
      firstBreak: true,
      observer: agent.provider === 'observer',
    });
  }

  refreshAgentTag(v) {
    if (!v) return;
    const sig = `${v.status}|${v.progressPct}|${v.activityText}|${v.queued}|${v.id === this.selectedId}`;
    if (v._tagSig === sig) return;
    v._tagSig = sig;
    const oldTex = v.label.material.map;
    const tagData = agentOverheadTag(v.name, {
      status: v.status,
      pct: v.progressPct,
      activity: v.activityText,
      queued: v.queued,
      isSelected: v.id === this.selectedId,
      deptColor: v.deptColor,
    });
    v.label.material.map = tagData.texture;
    v.label.material.needsUpdate = true;
    v.label.userData.aspect = tagData.aspect;
    v.label.userData.h = (v.status === 'working' || v.id === this.selectedId) ? 0.54 : 0.45;
    oldTex?.dispose?.();
  }

  setAgentProgress(id, { pct, activityText, queued, status } = {}) {
    const v = this.agents.get(id);
    if (!v) return;
    if (pct !== undefined) v.progressPct = pct;
    if (activityText !== undefined) v.activityText = activityText;
    if (queued !== undefined) v.queued = queued;
    if (status !== undefined && status !== v.status) this.setStatus(id, status, true);
    this.refreshAgentTag(v);
  }

  showBubble(id, text, accent = '#10b981', dur = 5.2) {
    const v = this.agents.get(id);
    if (!v || !v.bubble) return;
    const oldTex = v.bubble.material.map;
    const bData = speechBubbleTag(text, { accent });
    v.bubble.material.map = bData.texture;
    v.bubble.material.needsUpdate = true;
    v.bubble.userData.aspect = bData.aspect;
    v.bubble.visible = true;
    v.bubbleTimer = dur;
    oldTex?.dispose?.();
  }

  // ================================================================ giờ nghỉ & đi giao tiếp công việc
  updateLeisure(dt) {
    const k = dt * this.leisureSpeed;
    // Tự động kích hoạt trao đổi công việc định kỳ giữa Mama và các Subagent để văn phòng luôn sống động
    this.collabCooldown = (this.collabCooldown ?? 6) - dt;
    if (this.collabCooldown <= 0) {
      this.collabCooldown = rand(9, 15);
      this.triggerAmbientCollaboration();
    }

    if (!this.spots.length) return;
    for (const v of this.agents.values()) {
      const p = v.person;
      const free = v.status === 'idle';
      if (v.where === 'home') {
        if (!free || p.trip) { v.breakIn = null; continue; }
        v.breakIn ??= rand(...(v.firstBreak ? BREAK.first : BREAK.again));
        v.breakIn -= k;
        if (v.breakIn <= 0) { v.breakIn = null; v.firstBreak = false; this.goLeisure(v); }
      } else if (v.where === 'going' || v.where === 'leisure') {
        if (!free) { this.goHome(v, v.status !== 'offline'); continue; }
        if (v.where === 'leisure') {
          v.stay -= k;
          if (v.stay <= 0) Math.random() < 0.3 ? this.goLeisure(v) : this.goHome(v);
        }
      } else if (v.where === 'talking') {
        v.talkStay = (v.talkStay ?? 4) - dt;
        if (v.talkStay <= 0 || v.status === 'working') {
          v.person.talking = false;
          const peer = v.talkPeer ? this.agents.get(v.talkPeer) : null;
          if (peer) peer.person.talking = false;
          v.talkPeer = null;
          this.goHome(v, v.status === 'working');
        }
      }
    }
  }

  triggerAmbientCollaboration() {
    const pairs = [
      ['mama', 'mkt', '💬 Mama: Chốt 3 SKU Whitelist mới nhé!', '💬 MKT: Đã lọc xong ≥4.8 sao!'],
      ['mama', 'edit', '💬 Mama: Kiểm tra lưới Zero-Clone Page AI', '💬 Edit: 24/24 ảnh độc bản 100%!'],
      ['mama', 'edit-2', '💬 Mama: Chuẩn bị khung TVC 8 Nhịp Veo 3', '💬 Edit-2: Đã khóa Cảnh 3 Hero Reveal!'],
      ['edit', 'bo-nao-thu-2', '💬 Edit: Nhờ Bộ Não #2 duyệt mẫu mới', '💬 Bộ Não #2: APPROVED Luật #10 ✓'],
      ['mkt', 'content', '💬 MKT: Bàn giao insight KTX & Phòng Trọ', '💬 Content: Đang viết Hook 3s đầu!'],
      ['content', 'voice', '💬 Content: Kịch bản 32s vừa khớp nhịp', '💬 Voice: Đang mastering Vbee -3dB!'],
      ['quan-ly-kenh', 'cham-soc-kenh', '💬 QL Kênh: Lịch 11:45 & 20:00 đã lên', '💬 CS Kênh: Sẵn sàng Pinned Comment #1!'],
      ['hieu-suat', 'mama', '💬 Hiệu Suất: Báo cáo Funnel 4 Fanpage', '💬 Mama: Giữ vững nhịp độ đăng bài!'],
    ];
    const [fromId, toId, msgA, msgB] = pairs[Math.floor(Math.random() * pairs.length)];
    const a = this.agents.get(fromId), b = this.agents.get(toId);
    if (!a || !b) return;
    // Bắn tia truyền dữ liệu + cho nhân vật đi bộ sang trao đổi nếu đang ở bàn
    this.courier(fromId, toId, msgA.replace(/^💬\s*/, ''), fromId === 'mama' ? 'delegate' : toId === 'bo-nao-thu-2' ? 'audit' : 'chat');
    setTimeout(() => this.showBubble(toId, msgB, b.deptColor || '#06b6d4', 4.8), 1100);
    if (a.where === 'home' && !a.person.trip && a.status === 'idle') {
      this.walkToColleague(a, b, msgA, msgB);
    }
  }

  walkToColleague(visitor, host, msgVisitor, msgHost) {
    if (!visitor || !host || visitor.person.trip) return;
    const targetExit = host.home.exit;
    const path = this.nav?.findPath(visitor.home.exit.x, visitor.home.exit.z, targetExit.x, targetExit.z) ?? [visitor.home.exit, targetExit];
    const faceHost = faceToward(targetExit.x, targetExit.z, host.home.x, host.home.z);
    this.leaveSpot(visitor);
    visitor.where = 'walking_collab';
    visitor.person.travel({
      path,
      seat: { x: targetExit.x, z: targetExit.z, seatH: 0.68, facing: faceHost, variant: 'stand' },
      run: false,
      standAtEnd: true,
      onArrive: () => {
        visitor.where = 'talking';
        visitor.talkStay = 4.6;
        visitor.talkPeer = host.id;
        visitor.person.talking = true;
        host.person.talking = true;
        if (msgVisitor) this.showBubble(visitor.id, msgVisitor, visitor.deptColor || '#10b981', 4.5);
        if (msgHost) setTimeout(() => this.showBubble(host.id, msgHost, host.deptColor || '#38bdf8', 4.2), 900);
      },
    });
  }

  pickSpot(v) {
    const free = this.spots.filter(s => !s.occupant);
    if (!free.length) return null;
    const busy = new Map();
    for (const s of this.spots) if (s.occupant) busy.set(s.group, (busy.get(s.group) ?? 0) + 1);
    const cur = v.spot?.kind;
    const weights = free.map(s => (1 + 2.2 * (busy.get(s.group) ?? 0)) * (cur && s.kind === cur ? 0.35 : 1) * (s.variant === 'arcade' ? 0.8 : 1));
    let x = Math.random() * weights.reduce((a, b) => a + b, 0);
    for (let i = 0; i < free.length; i++) { x -= weights[i]; if (x <= 0) return free[i]; }
    return free[free.length - 1];
  }

  startPoint(v) {
    const p = v.person;
    if (p.trip) return { x: p.anchor.x, z: p.anchor.z };
    return v.where === 'home' ? v.home.exit : v.spot?.exit ?? { x: p.anchor.x, z: p.anchor.z };
  }

  route(v, seat) {
    const a = this.startPoint(v), b = seat.exit;
    const path = this.nav?.findPath(a.x, a.z, b.x, b.z) ?? [a, b];
    return path;
  }

  leaveSpot(v) {
    const s = v.spot; if (!s) return;
    if (v.where === 'leisure') { if (s.screen) s.screen.players = Math.max(0, s.screen.players - 1); s.cluster.occupants.delete(v.id); }
    s.occupant = null; v.spot = null;
    this.refreshLights();
    this.onLeisure?.();
  }

  leisureCounts() {
    const c = { cafe: 0, game: 0 };
    for (const v of this.agents.values()) if (v.where === 'leisure' && v.spot) c[v.spot.kind]++;
    return c;
  }

  goLeisure(v) {
    const seat = this.pickSpot(v);
    if (!seat) { v.where === 'home' || this.goHome(v); return; }
    const path = this.route(v, seat);
    this.leaveSpot(v);
    seat.occupant = v.id; v.spot = seat; v.where = 'going';
    v.person.travel({
      path, seat, run: false,
      onArrive: () => {
        v.where = 'leisure'; v.stay = rand(...BREAK.stay);
        if (seat.screen) seat.screen.players++;
        seat.cluster.occupants.add(v.id);
        this.refreshLights();
        this.onLeisure?.();
      },
    });
  }

  goHome(v, urgent = false) {
    const path = this.route(v, v.home);
    const dist = path.reduce((s, pt, i) => i ? s + Math.hypot(pt.x - path[i - 1].x, pt.z - path[i - 1].z) : 0, 0);
    this.leaveSpot(v);
    v.person.talking = false;
    v.where = 'returning';
    v.person.travel({
      path, seat: v.home, run: urgent && dist > 4,
      onArrive: () => { v.where = 'home'; v.breakIn = null; },
    });
  }

  syncAgent(v) {
    const p = v.person, a = p.anchor;
    if (v._ax === a.x && v._az === a.z && v._st === p.standing) return;
    v._ax = a.x; v._az = a.z; v._st = p.standing;
    const seatH = p.baseY ?? 0.5;
    const ly = (1.42 + seatH) * (1 - p.standing) + 2.12 * p.standing;
    v.label.position.set(a.x, ly, a.z);
    if (v.bubble) v.bubble.position.set(a.x, ly + 0.42, a.z);
    v.alert.position.x = a.x; v.alert.position.z = a.z; v.alertY = ly + 0.42;
    v.ring.position.set(a.x, 0.03, a.z);
    v.hit.position.set(a.x, 0.85 + 0.1 * p.standing, a.z); v.hit.rotation.y = p.root.rotation.y; v.hit.updateMatrixWorld(true);
    v.focus.set(a.x, 1.15 + 0.2 * p.standing, a.z);
    v.pos.set(a.x, 1.25, a.z);
  }

  setStatus(id, status, silent = false) {
    const v = this.agents.get(id);
    if (!v) return;
    const changed = v.status !== status;
    v.status = status;
    v.person.setStatus(status);
    v.screen.material = this.screens.material(v.theme, status);
    v.ring.material.color.set(STATUS_RING[status] ?? v.deptColor ?? '#10b981');
    v.alert.visible = status === 'waiting';
    if (status === 'working' && (!v.progressPct || v.progressPct < 10)) {
      v.progressPct = 20;
      if (!v.activityText || v.activityText === 'Sẵn sàng') v.activityText = '⚡ Đang thực thi...';
    } else if (status === 'idle') {
      v.progressPct = 0;
      v.activityText = 'Sẵn sàng';
    }
    this.updateLabel(v);
    if (changed && !silent) this.refreshLights();
  }

  updateLabel(v) {
    // Luôn hiển thị thẻ tên + trạng thái + % trên đầu mọi nhân vật 3D
    v.label.visible = true;
    this.refreshAgentTag(v);
    v.ring.userData.target = ['working', 'waiting', 'queued', 'error'].includes(v.status)
      ? 0.9
      : v.id === this.selectedId
        ? 0.75
        : v.id === this.hoveredId
          ? 0.5
          : 0.22;
  }

  select(id) {
    const prev = this.selectedId; this.selectedId = id;
    for (const k of [prev, id]) { const v = this.agents.get(k); if (v) this.updateLabel(v); }
  }

  refreshLights() {
    const busyOf = (c) => c.agents.reduce((s, id) => { const st = this.agents.get(id)?.status; return s + (st === 'working' ? 2 : st === 'waiting' ? 1.5 : st === 'queued' ? 0.5 : 0); }, 0);
    for (const c of this.clusters) {
      if (c.amenity) { const n = c.occupants.size; c.busy = n * 0.6; c.targetLevel = n ? 0.9 : 0.4; continue; }
      c.busy = busyOf(c);
      c.targetLevel = c.busy > 0 ? 1 : c.agents.length ? 0.38 : 0.18;
    }
    const ranked = [...this.clusters].sort((a, b) => b.busy - a.busy || b.agents.length - a.agents.length);
    this.pointLights.forEach((l, i) => {
      const c = ranked[i];
      if (!c) { l.userData.target = 0; return; }
      l.position.copy(c.center);
      l.userData.target = c.busy > 0 ? 10 : 3.2;
    });
  }

  /**
   * Hiệu ứng Truyền Thông Tin 3D bắt mắt (Mama <-> Subagent <-> Bộ Não Thứ 2):
   * - Đường cong ánh sáng năng lượng (Bezier Arc)
   * - Chuỗi 3 hạt xung dữ liệu phát sáng bay dọc theo đường cong
   * - Vòng sóng xung kích (Shockwave Ring) lan tỏa dưới chân bàn nhận lệnh
   * - Bong bóng hội thoại hiển thị nội dung trao đổi
   */
  courier(fromId, toId, topic = '', kind = 'delegate') {
    const va = this.agents.get(fromId), vb = this.agents.get(toId);
    const a = va?.pos, b = vb?.pos;
    if (!a || !b) return;

    const palette = {
      delegate: { beam: '#10b981', orb: '#6ee7b7', ring: '#34d399' },
      audit: { beam: '#06b6d4', orb: '#67e8f9', ring: '#22d3ee' },
      report: { beam: '#f59e0b', orb: '#fde68a', ring: '#fbbf24' },
      chat: { beam: '#8b5cf6', orb: '#c4b5fd', ring: '#a78bfa' },
    }[kind] || { beam: '#10b981', orb: '#6ee7b7', ring: '#34d399' };

    if (topic) {
      this.showBubble(fromId, `📨 ${topic}`, palette.beam, 4.2);
      setTimeout(() => this.showBubble(toId, `⚡ Đã nhận: ${topic}`, palette.ring, 4.2), 650);
    }

    const mid = a.clone().lerp(b, 0.5);
    mid.y += 2.6 + a.distanceTo(b) * 0.16;
    const curve = new THREE.QuadraticBezierCurve3(a.clone(), mid, b.clone());

    const dots = [0, 1, 2].map(() => {
      const m = new THREE.Mesh(
        new THREE.SphereGeometry(0.12, 14, 12),
        new THREE.MeshBasicMaterial({ color: palette.orb, toneMapped: false })
      );
      m.material.color.multiplyScalar(3.5);
      this.scene.add(m);
      return m;
    });

    const trail = new THREE.Line(
      new THREE.BufferGeometry().setFromPoints(curve.getPoints(56)),
      new THREE.LineBasicMaterial({ color: palette.beam, transparent: true, opacity: 0.78 })
    );
    const wave = new THREE.Mesh(
      new THREE.RingGeometry(0.35, 0.52, 40).rotateX(-Math.PI / 2),
      new THREE.MeshBasicMaterial({ color: palette.ring, transparent: true, opacity: 0.9, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false })
    );
    wave.position.set(b.x, 0.04, b.z);
    wave.renderOrder = 6;
    this.scene.add(trail, wave);
    this.couriers.push({ curve, dots, trail, wave, t: 0 });
  }

  // ================================================================ camera
  flyTo(id) {
    const v = this.agents.get(id); if (!v) return;
    const target = v.focus.clone();
    const dir = this.camera.position.clone().sub(this.controls.target).setY(0).normalize();
    this.animateCamera(target.clone().add(dir.multiplyScalar(4.2)).setY(target.y + 3.4), target);
  }
  overview() { this.animateCamera(this.home.pos.clone().multiplyScalar(this.homeScale ?? 1).setY(this.home.pos.y * (this.homeScale ?? 1)), this.home.target.clone()); }
  animateCamera(pos, target, dur = 0.9) {
    this.camAnim = { p0: this.camera.position.clone(), t0: this.controls.target.clone(), p1: pos, t1: target, t: 0, dur };
  }

  // ================================================================ chất lượng hình
  applyQuality(q, rebuild = true) {
    this.quality = q;
    try { localStorage.setItem('office.quality', q); } catch { /* bỏ qua */ }
    const r = this.renderer;
    r.setPixelRatio(Math.min(devicePixelRatio, q === 'high' ? 2 : q === 'medium' ? 1.5 : 1.25));
    r.shadowMap.enabled = q !== 'low';
    this.moon.castShadow = q !== 'low';
    const size = q === 'high' ? 2048 : 1024;
    if (this.moon.shadow.mapSize.x !== size) { this.moon.shadow.mapSize.set(size, size); this.moon.shadow.map?.dispose(); this.moon.shadow.map = null; }
    this.composer?.dispose?.();
    this.composer = null;
    if (q !== 'low') {
      const w = this.container.clientWidth || 800, h = this.container.clientHeight || 600;
      const target = new THREE.WebGLRenderTarget(w, h, { type: THREE.HalfFloatType, samples: q === 'high' ? 4 : 0 });
      const c = this.composer = new EffectComposer(r, target);
      c.addPass(new RenderPass(this.scene, this.camera));
      if (q === 'high') {
        const ao = new OfficeGTAO(this.scene, this.camera, w, h);
        ao.updateGtaoMaterial({ radius: 0.45, distanceExponent: 1.4, thickness: 1.2, scale: 1.1, samples: 12 });
        ao.updatePdMaterial({ lumaPhi: 10, depthPhi: 2, normalPhi: 3, radius: 6, rings: 2, samples: 12 });
        ao.blendIntensity = 0.85;
        c.addPass(ao);
      }
      c.addPass(this.bloom = new UnrealBloomPass(new THREE.Vector2(w, h), 0.38, 0.45, 0.82));
      c.addPass(new OutputPass());
    }
    this.applyShadows();
    if (rebuild && this.lastData) this.setData(...this.lastData);
    this.resize();
  }
  applyShadows() {
    const on = this.quality !== 'low';
    this.scene?.traverse(o => { if (o.isMesh && o.userData._cast === undefined) o.userData._cast = o.castShadow; if (o.isMesh) o.castShadow = on && o.userData._cast; });
  }

  // ================================================================ sự kiện chuột
  bindEvents() {
    const el = this.renderer.domElement;
    let down = null;
    const pick = (e) => {
      const rect = el.getBoundingClientRect();
      this.pointer.set(((e.clientX - rect.left) / rect.width) * 2 - 1, -((e.clientY - rect.top) / rect.height) * 2 + 1);
      this.raycaster.setFromCamera(this.pointer, this.camera);
      return this.raycaster.intersectObjects(this.hitboxes, false)[0]?.object.userData.agentId ?? null;
    };
    el.addEventListener('pointerdown', e => { down = [e.clientX, e.clientY]; this.camAnim = null; });
    el.addEventListener('pointerup', e => {
      if (!down || Math.hypot(e.clientX - down[0], e.clientY - down[1]) > 6) return;
      const id = pick(e); if (id) this.onPick?.(id);
    });
    el.addEventListener('dblclick', e => { const id = pick(e); if (id) this.flyTo(id); });
    el.addEventListener('pointermove', e => {
      if (e.buttons) return;
      const id = pick(e);
      if (id === this.hoveredId) return;
      const prev = this.hoveredId; this.hoveredId = id;
      for (const k of [prev, id]) { const v = this.agents.get(k); if (v) { this.updateLabel(v); v.person.mat.emissive.set(k === id && v.status !== 'error' ? '#2a1d0c' : v.status === 'error' ? '#3a0606' : '#000'); } }
      el.style.cursor = id ? 'pointer' : 'grab';
      this.onHover?.(id);
    });
  }

  resize(force = false) {
    const w = this.container.clientWidth, h = this.container.clientHeight;
    if (!w || !h) return;
    this.renderer.setSize(w, h);
    this.composer?.setSize(w, h);
    this.camera.aspect = w / h;
    this.camera.updateProjectionMatrix();
    const scale = this.camera.aspect < 1.25 ? Math.min(2.1, 1.25 / this.camera.aspect) : 1;
    if (force || this.homeScale !== scale) {
      this.homeScale = scale;
      this.camera.position.copy(this.home.pos).multiplyScalar(scale).setY(this.home.pos.y * scale);
      this.controls.target.copy(this.home.target);
    }
  }

  // ================================================================ vòng lặp
  frame() {
    if (this.paused) return;
    this.step(Math.min(0.05, this.clock.getDelta()));
  }

  debugRender(steps = 60, dt = 1 / 30) {
    this.paused = true;
    this.autoQuality = false;
    for (let i = 0; i < steps; i++) this.step(dt, i === steps - 1);
  }

  step(dt, render = true) {
    this.simTime = (this.simTime ?? 0) + dt;
    const t = this.simTime;
    this.screens.update(t);
    this.games.update(t);
    this.updateLeisure(dt);
    for (const v of this.agents.values()) {
      v.person.update(t, dt);
      this.syncAgent(v);
      if (v.bubbleTimer > 0) {
        v.bubbleTimer -= dt;
        if (v.bubbleTimer <= 0 && v.bubble) v.bubble.visible = false;
      }
      const m = v.ring.material, tgt = v.ring.userData.target ?? 0.22;
      m.opacity += (tgt - m.opacity) * Math.min(1, dt * 6);
      v.ring.visible = m.opacity > 0.01;
      if (v.ring.visible) { const s = 1 + (Math.sin(t * 3 + v.pos.x) + 1) * 0.07; v.ring.scale.set(s, 1, s); }
      if (v.alert.visible) v.alert.position.y = (v.alertY ?? v.person.baseY + 1.8) + Math.sin(t * 5) * 0.05;
      for (const sp of [v.label, v.bubble, v.alert]) {
        if (!sp || !sp.visible) continue;
        const d = this.camera.position.distanceTo(sp.position);
        const h = Math.min(sp.userData.h * 1.35, Math.max(0.28, d * 0.024 * (sp.userData.h / 0.45)));
        sp.scale.set(h * sp.userData.aspect, h, 1);
      }
    }
    for (const c of this.clusters) {
      c.level = (c.level ?? 0) + ((c.targetLevel ?? 0.2) - (c.level ?? 0)) * Math.min(1, dt * 2.5);
      const L = c.level;
      for (const lamp of c.lamps) lamp.bulb.material.color.setRGB(0.6 + 2.6 * L, 0.45 + 2.0 * L, 0.3 + 1.2 * L);
      if (c.poolMat) c.poolMat.opacity = 0.05 + 0.3 * L;
    }
    for (const l of this.pointLights) l.intensity += (l.userData.target - l.intensity) * Math.min(1, dt * 2.5);
    // Tia truyền dữ liệu 3D đa hạt + vòng sóng xung kích
    for (let i = this.couriers.length - 1; i >= 0; i--) {
      const c = this.couriers[i];
      c.t += dt / 1.45;
      if (c.t >= 1) {
        c.dots.forEach(d => { this.scene.remove(d); d.geometry.dispose(); d.material.dispose(); });
        this.scene.remove(c.trail, c.wave);
        c.trail.geometry.dispose(); c.trail.material.dispose();
        c.wave.geometry.dispose(); c.wave.material.dispose();
        this.couriers.splice(i, 1);
        continue;
      }
      c.dots.forEach((d, idx) => {
        const ptT = Math.max(0, Math.min(1, c.t * 1.15 - idx * 0.12));
        d.position.copy(c.curve.getPoint(ptT));
      });
      c.trail.material.opacity = 0.78 * (1 - Math.pow(c.t, 1.5));
      const ws = 1 + c.t * 2.6;
      c.wave.scale.set(ws, 1, ws);
      c.wave.material.opacity = 0.9 * (1 - c.t);
    }
    if (this.camAnim) {
      const a = this.camAnim; a.t += dt / a.dur;
      const k = a.t >= 1 ? 1 : 1 - Math.pow(1 - a.t, 3);
      this.camera.position.lerpVectors(a.p0, a.p1, k);
      this.controls.target.lerpVectors(a.t0, a.t1, k);
      if (a.t >= 1) this.camAnim = null;
    }
    this.controls.update();
    if (!render) return;
    this.renderer.info.reset();
    if (this.composer) this.composer.render(dt); else this.renderer.render(this.scene, this.camera);
    this.watchFps(dt);
  }

  /** Tự hạ chất lượng nếu FPS trung bình 3 giây < 30 */
  watchFps(dt) {
    const f = this.fps;
    f.frames++; f.acc += dt;
    if (f.acc < 3) return;
    const fpsAvg = f.frames / f.acc;
    this.lastFps = fpsAvg;
    f.frames = 0; f.acc = 0;
    if (this.autoQuality !== false && fpsAvg < 30 && this.quality !== 'low' && performance.now() - f.lastDowngrade > 8000) {
      f.lastDowngrade = performance.now();
      this.applyQuality(this.quality === 'high' ? 'medium' : 'low');
      this.onQualityAuto?.(this.quality);
    }
  }

  stats() {
    const i = this.renderer.info;
    return { calls: i.render.calls, triangles: i.render.triangles, geometries: i.memory.geometries, textures: i.memory.textures, fps: this.lastFps };
  }
}
