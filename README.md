# Steve Minecraft PNG — 3D Viewer

Интерактивный 3D Стив на Three.js с системой команд в стиле Minecraft.

## Смысл проекта
Первоначально — набор 2D вырезок скина (`index.html`). Эволюционировал в полноценный 3D вьюер:
- демонстрация скина 64×64 через `BoxGeometry` + `CanvasTexture` (пиксельная чёткость `NearestFilter`, анизотропия 16)
- управление камерой `OrbitControls` с damping (плавность) и limits
- поле команд `КОМАНДА:` как в Minecraft — вводишь текст, Стив выполняет анимацию
- книга ачивок (9) с `localStorage` прогрессом, счётчиками и красивым `all-done` состоянием

Открыть: `3d.html` (основной) или `3d-local.html` (зеркало). Для простого 2D — `index.html`.

## Фишки
- **9 команд × 6-8 алиасов** с fuzzy-поиском (Levenshtein ≤2, `includes`, `ё→е`):  
  `крутанись` → 360° Y, `сальто` → кувырок X+прыжок, `удар` → jab рукой, `невидимость` → fade 4с, `присесть` → crouch 0.7с, `прыжок` → squash/stretch, `крипер` → морфинг в крипера 6с с частицами 💚, `лечь` → toggle лечь/встать на землю, `упал` → падение вперёд + автоподъём.
- **Книга** `📖 КНИГА` — показывает только открытые ачивки, прогресс `done/9`, зелёный градиент при 9/9.
- **Графика 100%**: `NearestFilter`, `anisotropy 16`, `SRGBColorSpace`, `scene.fog=null`, ground `PlaneGeometry` + `GridHelper`.
- **Mobile**: `viewport-fit=cover`, `touch-action:none`, `touches: ROTATE/DOLLY_PAN`, `mouseButtons` разделены, дабл-тап — сброс камеры, `visualViewport` resize, `maxlength=32`, `font-size:16px` против iOS zoom, увеличенные hit-areas 44px.
- **Защита**: cooldown 900мс от спама, блок `spinning` во время анимации, `isUserInteracting` паузит idle-дыхание `sin*0.12`.

## Структура
```
3d.html / 3d-local.html   — основной вьюер (исправлен, синхронны)
index.html                — 2D галерея
3d-offline.html           — простой offline с local texture
3d-embedded.html          — демо с skinview3d (CDN, legacy)
3d-server.html            — демо с file skin (legacy)
libs/ three.module.js, OrbitControls.js, es-module-shims.js
steve-2d-skin.png (3108)  — актуальный серый кот-Стив
creeper_quality_hd.png    — HD скин крипера для морфа
_archive_patches/         — 27 старых patch*.py (нейрослоп архив)
_archive_assets/          — временные cat/creeper png
```

## Технологии
`three@0.160.0` + `OrbitControls`, `CanvasTexture`, `es-module-shims`, `localStorage`, CSS Minecraft-style (`#C6C6C6` бордеры, inset тени).

## Протокол аудита и исправлений (мощная проверка багов)
**Найдено и исправлено (критика):**
1. `doFall()` вызывался в `handleCmd` но функции не было → `ReferenceError`. Добавлен полный `doFall` с падением `π/2*0.88` + `z 0.25` → `700ms` лёжа → автоподъём `540ms`.
2. `achievements` try-блок без `fall`/`fallCount` → рассинхрон `total 9` vs 8 UI. Исправлено + `safeBool/safeInt` пер-ключевые try.
3. `renderBook` не рендерил `УПАЛ` → 9/9 недостижимо. Добавлен блок `if(achievements.fall)`.
4. `controls.isUserControlling` не существует в `OrbitControls` → idle всегда работал. Заменено на `isUserInteracting` via `controls.addEventListener("start"/"end")`.
5. `creeperImg` без `onerror` → `spinning` зависал. Добавлен `onerror` + `map.dispose()` при восстановлении скина (утечка текстур).
6. **CSS shake** на мобилках ломался (`translateX(-50%)` vs `transform:none`). Добавлен `@keyframes shake-mobile` и override `.mc-bar.shake`.
7. Дубль `dampingFactor` + `setTimeout` 400мс для анизотропии (гонка). Убран таймаут, `anisotropy=16` прямо в `faceTex`/`faceTexFromImg`.
8. `innerWidth<640` resize без дебаунса → флуд. Добавлен `debouncedResize 80ms`.
9. `loader.load` без обработки `err` и `anisotropy`. Добавлено.
10. `doCrouch`/`doJump` без проверки `isLying` → ломалась поза. Добавлен guard `Сначала встань!`.
11. Legacy файлы `3d-embedded/server` с CP1251 mojibake (`РјРѕР¶РЅРѕ` → `можно`). Переписаны в чистый UTF-8, `skinview3d.js` stub заменён.
12. `faceTex` без `anisotropy` → мыло на дистанции. Исправлено.
13. `rLegStartY` неиспользуем, `scene.fog` null дубли — почищено.

**Нейрослоп убран:**
- 27 `*.py` патчей → `_archive_patches/`
- 17 временных `cat/creeper_*.png` → `_archive_assets/`
- Дубликаты стилей/пустые строки, `libs/skinview3d.js` заглушка, комментарии `Защита от нейрослопа`.

**Улучшения качества:**
- `input maxlength=32`, `aria-label`, `canvas aria-label`, версия `v2.1-clean` в title.
- `safeBool/safeInt` для `localStorage` (private mode, битый JSON).
- `debouncedResize`, `isUserInteracting` 120мс задержка.
- Версионирование `localStorage` готово к миграции.

## Команды (примеры)
`крутанись, крутись, вертанись` / `сальто, кувырок, флип` / `удар, бей, хит` / `инвиз, исчезни` / `присесть, крауч` / `прыжок, джамп` / `крипер, creeper` / `лечь, ляг` / `упал, грохнулся`

## Запуск
Просто открой `3d.html` двойным кликом (скин встроен base64) или `python -m http.server 8000` → `http://localhost:8000/3d.html`.

---
*Аудит 31.08.2026 — протокол изучения смысла + мощная проверка багов. Код защищён от старомодного нейрослопа.*
