// Interactive KNUST campus map (Leaflet + OpenStreetMap tiles).
// Dispatches a bubbling 'venue-select' CustomEvent; call setSelected(name) to sync from outside.
(function () {
  const VENUES = [
    { n: 1, name: 'Great Hall', lat: 6.67475, lng: -1.57220, dir: 'right', stem: 24 },
    { n: 2, name: 'Paa Joe Stadium', lat: 6.67780, lng: -1.56950, dir: 'right', stem: 28 },
    { n: 3, name: 'College of Science Auditorium', lat: 6.67350, lng: -1.56650, dir: 'right', stem: 26 },
    { n: 4, name: 'Prempeh II Library', lat: 6.67510, lng: -1.57180, dir: 'left', stem: 34 },
    { n: 5, name: 'KNUST Interdenominational Church', lat: 6.68508, lng: -1.57270, dir: 'right', stem: 28 },
    { n: 6, name: 'KNUST Campus', lat: 6.67644, lng: -1.57343, dir: 'left', stem: 24 }
  ];

  const icon = (n, on) => L.divIcon({
    className: '',
    iconSize: [30, 30],
    iconAnchor: [15, 15],
    html:
      '<div style="width:30px;height:30px;display:flex;align-items:center;justify-content:center;' +
      'font-family:\'JetBrains Mono\',monospace;font-size:13px;font-weight:600;color:#fff;' +
      'border:1px solid #201e1d;background:' + (on ? '#1a3ee8' : '#201e1d') + '">' + n + '</div>'
  });

  // Category tokens live in eventweb.css. divIcon markup is inserted into the
  // document, so var() resolves here and the palette stays in one place.
  const CAT_VAR = {
    Academic: 'var(--ew-cat-academic, #1a3ee8)',
    Social: 'var(--ew-cat-social, #b3261e)',
    Sports: 'var(--ew-cat-sports, #0b6b3a)',
    Religious: 'var(--ew-cat-religious, #6b3fa0)',
    Business: 'var(--ew-cat-business, #8a5a00)'
  };
  const INK = '#101215';
  const FONT = "font-family:'Archivo',system-ui,sans-serif;";

  // Option B: Drafting callout marker.
  // An architect's leader line: a 2px stem pinned to the exact coordinate,
  // carrying a flat label with the venue number and category colour bar.
  const callout = (v, on, d) => {
    const venueName = v.name || '';
    const label = venueName.replace('KNUST ', '');
    const bar = d && d.cat ? (CAT_VAR[d.cat] || 'var(--ew-accent, #1a3ee8)') : (d ? 'var(--ew-accent, #1a3ee8)' : 'var(--ew-neutral-400, #9aa0aa)');
    const isLeft = v.dir === 'left';
    const stemH = v.stem || 26;
    const flagPos = isLeft ? `right:0;bottom:${stemH}px` : `left:0;bottom:${stemH}px`;
    const flagContent = isLeft
      ? `<span style="${FONT}font-size:11px;font-weight:600;padding:3px 0 3px 7px;color:${on ? 'var(--ew-bg, #fff)' : 'var(--ew-text-label, #4b5160)'}">${label}</span>` +
        `<span style="${FONT}font-size:11px;font-weight:800;padding:3px 6px;color:${on ? 'var(--ew-bg, #fff)' : 'var(--ew-ink, #101215)'}">${v.n}</span>` +
        `<span style="width:5px;flex-shrink:0;background:${bar}"></span>`
      : `<span style="width:5px;flex-shrink:0;background:${bar}"></span>` +
        `<span style="${FONT}font-size:11px;font-weight:800;padding:3px 6px;color:${on ? 'var(--ew-bg, #fff)' : 'var(--ew-ink, #101215)'}">${v.n}</span>` +
        `<span style="${FONT}font-size:11px;font-weight:600;padding:3px 7px 3px 0;color:${on ? 'var(--ew-bg, #fff)' : 'var(--ew-text-label, #4b5160)'}">${label}</span>`;

    return L.divIcon({
      className: '',
      iconSize: [0, 0],
      iconAnchor: [0, 0],
      html:
        '<span style="position:absolute;left:0;bottom:0;display:block">' +
          `<span style="position:absolute;left:0;bottom:0;width:2px;height:${stemH}px;background:var(--ew-ink, #101215)"></span>` +
          `<span style="position:absolute;${flagPos};display:flex;align-items:stretch;` +
            `border:1px solid var(--ew-rule-color, #101215);background:${on ? 'var(--ew-ink, #101215)' : 'var(--ew-bg, #fff)'};white-space:nowrap;` +
            `box-shadow:0 2px 8px rgba(0,0,0,${on ? '0.35' : '0.15'})">` +
            flagContent +
          '</span>' +
        '</span>'
    });
  };

  class KnustMap extends HTMLElement {
    connectedCallback() {
      // may already be populated by a setVenueData() call made before upgrade
      this._data = this._data || {};
      this._selected = this._selected || null;
      if (this._built) return;
      this._built = true;
      this.style.display = 'block';
      this.style.width = '100%';
      this.style.height = '100%';
      this.style.minHeight = '560px';
      const wait = () => {
        if (typeof L === 'undefined') return setTimeout(wait, 60);
        this._build();
      };
      wait();

      this._themeListener = () => this._refresh();
      window.addEventListener('theme-change', this._themeListener);
    }

    _build() {
      const map = L.map(this, {
        center: [6.6762, -1.5715],
        zoom: 15,
        scrollWheelZoom: false,
        attributionControl: true
      });
      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
      }).addTo(map);

      this._markers = {};
      VENUES.forEach(v => {
        const d = this._data[v.name];
        const m = L.marker([v.lat, v.lng], {
          icon: callout(v, false, d),
          title: v.name,
          alt: this._describe(v, d)
        }).addTo(map);
        m.bindTooltip(this._describe(v, d), { direction: 'top', offset: [0, -30] });
        m.on('click', () => {
          this.dispatchEvent(new CustomEvent('venue-select', {
            bubbles: true, composed: true, detail: { name: v.name }
          }));
        });
        this._markers[v.name] = { marker: m, n: v.n, lat: v.lat, lng: v.lng, dir: v.dir, stem: v.stem };
      });

      this._map = map;
      setTimeout(() => map.invalidateSize(), 120);

      // The element can be laid out after Leaflet has already measured it
      // (stylesheet arriving late, a re-render, or the pane being resized),
      // which otherwise leaves the tiles and controls mispositioned.
      if (typeof ResizeObserver !== 'undefined') {
        this._ro = new ResizeObserver(() => map.invalidateSize());
        this._ro.observe(this);
      }
    }

    disconnectedCallback() {
      if (this._ro) { this._ro.disconnect(); this._ro = null; }
      if (this._themeListener) { window.removeEventListener('theme-change', this._themeListener); this._themeListener = null; }
    }

    // What is on at each venue, keyed by venue name:
    //   { 'Great Hall': { cat, poster, title, initials }, ... }
    // Venues absent from the object read as "nothing booked yet". Safe to call
    // before the map has built — the data is kept and applied on build.
    setVenueData(data) {
      this._data = data || {};
      if (this._map) this._refresh();
    }

    _describe(v, d) {
      if (!d) return v.name + ' — nothing booked yet';
      return v.name + ' — ' + (d.title || d.cat || 'one event');
    }

    _refresh() {
      if (!this._markers) return;
      Object.keys(this._markers).forEach(k => {
        const e = this._markers[k];
        const d = this._data[k];
        const v = { n: e.n, name: k, dir: e.dir, stem: e.stem };
        e.marker.setIcon(callout(v, k === this._selected, d));
        const text = this._describe({ name: k }, d);
        e.marker.setTooltipContent(text);
      });
    }

    setSelected(name) {
      if (!this._markers) return;
      this._selected = name;
      Object.keys(this._markers).forEach(k => {
        const e = this._markers[k];
        e.marker.setIcon(callout({ n: e.n, name: k, dir: e.dir, stem: e.stem }, k === name, this._data[k]));
      });
      const sel = name && this._markers[name];
      if (sel && this._map) this._map.flyTo([sel.lat, sel.lng], 16, { duration: 0.6 });
      else if (this._map) this._map.flyTo([6.6762, -1.5715], 15, { duration: 0.6 });
    }
  }

  if (!customElements.get('knust-map')) customElements.define('knust-map', KnustMap);
})();
