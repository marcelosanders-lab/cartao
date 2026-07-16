/* ============================================================
   SANBERG — Logos, graphic elements, icons (React)
   Exposes components on window for other babel scripts.
   ============================================================ */

/* ---- Typographic serif "S" monogram (crisp, reliable) ---- */
function SerifS({ size, color, weight = 500 }){
  return (
    <span style={{
      fontFamily:"'Spectral', Georgia, serif", fontWeight:weight, color,
      fontSize: size, lineHeight:1, display:'block', userSelect:'none'
    }}>S</span>
  );
}

/* ---- Concept 1 · PÓRTICO — serif S in a double-rule frame (traditional/structured) ---- */
function MarkPortico({ size = 64, ink = '#0E2A45', accent = '#C19A4B' }){
  return (
    <div style={{position:'relative', width:size, height:size}} role="img" aria-label="Sanberg monograma Pórtico">
      <svg width={size} height={size} viewBox="0 0 64 64" style={{position:'absolute', inset:0}}>
        <rect x="2.5" y="2.5" width="59" height="59" rx="2" fill="none" stroke={ink} strokeWidth="2"/>
        <rect x="6.5" y="6.5" width="51" height="51" rx="1" fill="none" stroke={accent} strokeWidth="0.9"/>
      </svg>
      <div style={{position:'absolute', inset:0, display:'grid', placeItems:'center'}}>
        <SerifS size={size*0.62} color={ink}/>
      </div>
    </div>
  );
}

/* ---- Concept 2 · ÉGIDE — serif S within a shield (security/protection) ---- */
function MarkEgide({ size = 64, ink = '#0E2A45', accent = '#C19A4B', glyph = '#FFFFFF' }){
  return (
    <div style={{position:'relative', width:size, height:size}} role="img" aria-label="Sanberg monograma Égide">
      <svg width={size} height={size} viewBox="0 0 64 64" style={{position:'absolute', inset:0}}>
        <path d="M32 3 L57 11 L57 31 C57 46 46 56 32 61 C18 56 7 46 7 31 L7 11 Z" fill={ink}/>
        <path d="M32 8 L52 14.4 L52 30 C52 42 44 50 32 54.5 C20 50 12 42 12 30 L12 14.4 Z"
              fill="none" stroke={accent} strokeWidth="1.1"/>
      </svg>
      <div style={{position:'absolute', inset:0, display:'grid', placeItems:'center', paddingBottom:size*0.04}}>
        <SerifS size={size*0.52} color={glyph}/>
      </div>
    </div>
  );
}

/* ---- Concept 3 · VÉRTICE — staggered bars tracing an S-ascent (modern/tech) ---- */
function MarkVertice({ size = 64, ink = '#0E2A45', accent = '#C19A4B' }){
  return (
    <svg width={size} height={size} viewBox="0 0 64 64" role="img" aria-label="Sanberg monograma Vértice">
      <rect x="24" y="11" width="28" height="8" rx="4" fill={ink}/>
      <rect x="14" y="28" width="36" height="8" rx="4" fill={accent}/>
      <rect x="12" y="45" width="28" height="8" rx="4" fill={ink}/>
      <circle cx="50" cy="15" r="4" fill={accent}/>
      <circle cx="14" cy="49" r="4" fill={accent}/>
    </svg>
  );
}

/* ---- Lockup: mark + wordmark (HTML text, directly editable) ---- */
function Lockup({ which = 'vertice', ink = '#0E2A45', accent = '#C19A4B', sub = '#6E8497',
                  orientation = 'horizontal', size = 56, showSub = true, name = 'Sanberg' }){
  const Mark = (which === 'portico') ? MarkPortico : (which === 'egide') ? MarkEgide : MarkVertice;
  const vertical = orientation === 'vertical';
  return (
    <div style={{
      display:'flex', alignItems:'center', gap: vertical ? 12 : 16,
      flexDirection: vertical ? 'column' : 'row', textAlign: vertical ? 'center':'left'
    }}>
      <Mark size={size} ink={ink} accent={accent}/>
      <div style={{lineHeight:1}}>
        <div style={{
          fontFamily:"'Spectral', serif", fontWeight:600, color:ink,
          fontSize: size*0.5, letterSpacing:'.01em', lineHeight:1
        }}>{name}</div>
        {showSub &&
          <div style={{
            fontFamily:"'IBM Plex Mono', monospace", color:sub,
            fontSize: Math.max(8, size*0.135), letterSpacing:'.34em',
            textTransform:'uppercase', marginTop: size*0.13
          }}>Soluções Jurídicas</div>}
      </div>
    </div>
  );
}

/* ---- Graphic element: precision line motif (the "Malha") ---- */
function MalhaPattern({ stroke = '#C19A4B', bg = 'transparent', w = 320, h = 180, op = 0.5 }){
  const lines = [];
  for(let i=0;i<=8;i++){
    const x = (w/8)*i;
    lines.push(<line key={'v'+i} x1={x} y1="0" x2={x} y2={h} stroke={stroke} strokeWidth="0.6" opacity={op*0.5}/>);
  }
  return (
    <svg width="100%" viewBox={`0 0 ${w} ${h}`} preserveAspectRatio="none" style={{display:'block'}}>
      <rect width={w} height={h} fill={bg}/>
      {lines}
      <path d={`M0 ${h} L${w*0.34} ${h*0.32} L${w*0.58} ${h*0.62} L${w} ${h*0.12}`}
            fill="none" stroke={stroke} strokeWidth="1.6" opacity={op}/>
      <circle cx={w*0.34} cy={h*0.32} r="3.4" fill={stroke}/>
      <circle cx={w} cy={h*0.12} r="3.4" fill={stroke}/>
    </svg>
  );
}

/* ---- Corner rule / framing device ---- */
function CornerRule({ color = '#C19A4B', size = 40, sw = 1.4 }){
  return (
    <svg width={size} height={size} viewBox="0 0 40 40">
      <path d={`M2 14 L2 2 L14 2`} fill="none" stroke={color} strokeWidth={sw}/>
      <path d={`M38 26 L38 38 L26 38`} fill="none" stroke={color} strokeWidth={sw}/>
    </svg>
  );
}

/* ---- Custom service icons (geometric line set) ---- */
function Icon({ name, size = 40, color = '#0E2A45', accent = '#C19A4B' }){
  const p = { fill:'none', stroke:color, strokeWidth:1.6, strokeLinecap:'round', strokeLinejoin:'round' };
  const a = { fill:'none', stroke:accent, strokeWidth:1.6, strokeLinecap:'round', strokeLinejoin:'round' };
  const icons = {
    /* Consultoria jurídica — balança */
    consultoria: (<g>
      <line x1="20" y1="6" x2="20" y2="34" {...p}/>
      <line x1="10" y1="11" x2="30" y2="11" {...p}/>
      <path d="M10 11 L5 22 L15 22 Z" {...a}/>
      <path d="M30 11 L25 22 L35 22 Z" {...p}/>
      <line x1="13" y1="34" x2="27" y2="34" {...p}/>
    </g>),
    /* Tributário/fiscal — documento % */
    tributario: (<g>
      <rect x="9" y="6" width="22" height="28" rx="2" {...p}/>
      <line x1="14" y1="14" x2="22" y2="14" {...p}/>
      <circle cx="16" cy="22" r="2.4" {...a}/>
      <circle cx="24" cy="28" r="2.4" {...p}/>
      <line x1="15" y1="29" x2="25" y2="21" {...a}/>
    </g>),
    /* Contencioso/litígio — pilares tribunal */
    contencioso: (<g>
      <path d="M7 14 L20 7 L33 14" {...p}/>
      <line x1="11" y1="17" x2="11" y2="29" {...p}/>
      <line x1="20" y1="17" x2="20" y2="29" {...a}/>
      <line x1="29" y1="17" x2="29" y2="29" {...p}/>
      <line x1="7" y1="33" x2="33" y2="33" {...p}/>
    </g>),
    /* Saúde suplementar — escudo + cruz */
    saude: (<g>
      <path d="M20 6 L31 10 L31 21 C31 28 26 31 20 34 C14 31 9 28 9 21 L9 10 Z" {...p}/>
      <line x1="20" y1="15" x2="20" y2="25" {...a}/>
      <line x1="15" y1="20" x2="25" y2="20" {...a}/>
    </g>),
    /* Inovação — node */
    inovacao: (<g>
      <circle cx="20" cy="20" r="4" {...a}/>
      <circle cx="9" cy="11" r="2.6" {...p}/>
      <circle cx="31" cy="11" r="2.6" {...p}/>
      <circle cx="9" cy="29" r="2.6" {...p}/>
      <circle cx="31" cy="29" r="2.6" {...p}/>
      <line x1="11.5" y1="12.5" x2="17" y2="17.5" {...p}/>
      <line x1="28.5" y1="12.5" x2="23" y2="17.5" {...p}/>
      <line x1="11.5" y1="27.5" x2="17" y2="22.5" {...p}/>
      <line x1="28.5" y1="27.5" x2="23" y2="22.5" {...p}/>
    </g>),
    /* Confidencialidade — cadeado */
    seguranca: (<g>
      <rect x="10" y="18" width="20" height="16" rx="2" {...p}/>
      <path d="M14 18 v-3 a6 6 0 0 1 12 0 v3" {...p}/>
      <circle cx="20" cy="25" r="2.2" {...a}/>
      <line x1="20" y1="27" x2="20" y2="30" {...a}/>
    </g>),
  };
  return (<svg width={size} height={size} viewBox="0 0 40 40" role="img" aria-label={name}>{icons[name] || null}</svg>);
}

Object.assign(window, {
  SerifS, MarkPortico, MarkEgide, MarkVertice, Lockup,
  MalhaPattern, CornerRule, Icon
});
