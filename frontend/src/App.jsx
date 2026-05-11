/**
 * App.jsx — Frontend Pixel Art Studio
 * Ne contient AUCUNE logique de dessin.
 * Envoie des requêtes GET à l'API Flask et rend les pixels sur canvas.
 */
import { useState, useRef, useEffect } from "react"

const API  = "http://localhost:5000/api"
const CW = 9, CH = 15, COLS = 72, ROWS = 36
const W = COLS * CW, H = ROWS * CH

const IMAGES = [
  { id:"soleil",   label:"☀  Soleil"   },
  { id:"coeur",    label:"♥  Cœur"     },
  { id:"maison",   label:"⌂  Maison"   },
  { id:"montagne", label:"⛰  Montagne" },
  { id:"flocon",   label:"❄  Flocon"   },
]
const ANIMS = [
  { id:"soleil",  label:"☀  Soleil tournant" },
  { id:"pluie",   label:"⬇  Pluie Matrix"   },
  { id:"vague",   label:"〜  Vagues de mer"  },
  { id:"feu",     label:"🔥  Feu"             },
  { id:"flocons", label:"❄  Flocons"          },
]

function dessinerPixels(ctx, pixels) {
  ctx.fillStyle = "#080b10"; ctx.fillRect(0,0,W,H)
  ctx.font = `${CW+2}px 'Courier New',monospace`
  ctx.textAlign="left"; ctx.textBaseline="top"
  for (const {x,y,c,r,g,b} of pixels) {
    ctx.fillStyle=`rgb(${r},${g},${b})`; ctx.fillText(c,x*CW,y*CH)
  }
  ctx.fillStyle="rgba(0,0,0,0.07)"
  for (let ly=0;ly<H;ly+=2) ctx.fillRect(0,ly,W,1)
}
function placeholder(ctx, msg) {
  ctx.fillStyle="#080b10"; ctx.fillRect(0,0,W,H)
  ctx.fillStyle="rgba(0,200,80,0.22)"; ctx.font="13px 'Courier New',monospace"
  ctx.textAlign="center"; ctx.textBaseline="middle"; ctx.fillText(msg,W/2,H/2)
}

function ImageCanvas({ pixels }) {
  const ref=useRef(null), timer=useRef(null)
  useEffect(()=>{
    const ctx=ref.current.getContext("2d")
    ref.current.width=W; ref.current.height=H
    placeholder(ctx,"Sélectionne une image  →  GÉNÉRER")
  },[])
  useEffect(()=>{
    if (!pixels) return
    if (timer.current) clearInterval(timer.current)
    const ctx=ref.current.getContext("2d")
    const parLigne={}
    for (const p of pixels) { if (!parLigne[p.y]) parLigne[p.y]=[]; parLigne[p.y].push(p) }
    let ligne=0
    timer.current=setInterval(()=>{
      ctx.fillStyle="#080b10"; ctx.fillRect(0,0,W,H)
      ctx.font=`${CW+2}px 'Courier New',monospace`; ctx.textAlign="left"; ctx.textBaseline="top"
      for (let y=0;y<=ligne;y++)
        for (const {x,y:py,c,r,g,b} of (parLigne[y]||[])) {
          ctx.fillStyle=`rgb(${r},${g},${b})`; ctx.fillText(c,x*CW,py*CH)
        }
      ctx.fillStyle="rgba(0,0,0,0.07)"
      for (let ly=0;ly<H;ly+=2) ctx.fillRect(0,ly,W,1)
      ligne++; if (ligne>=ROWS) clearInterval(timer.current)
    },18)
    return ()=>clearInterval(timer.current)
  },[pixels])
  return <canvas ref={ref} style={CS}/>
}

function AnimCanvas({ animId, running }) {
  const ref=useRef(null), frameRef=useRef(0), stopRef=useRef(false)
  useEffect(()=>{
    const ctx=ref.current.getContext("2d")
    ref.current.width=W; ref.current.height=H
    placeholder(ctx,"▶  Lance une animation")
  },[])
  useEffect(()=>{
    const ctx=ref.current.getContext("2d")
    stopRef.current=!running
    if (!running) { placeholder(ctx,"▶  Lance une animation"); return }
    frameRef.current=0; stopRef.current=false
    async function boucle() {
      if (stopRef.current) return
      try {
        const res=await fetch(`${API}/animer/${animId}/${frameRef.current}`)
        const data=await res.json()
        if (data.pixels && !stopRef.current) { dessinerPixels(ctx,data.pixels); frameRef.current++ }
      } catch(e) { stopRef.current=true; return }
      if (!stopRef.current) requestAnimationFrame(boucle)
    }
    requestAnimationFrame(boucle)
    return ()=>{ stopRef.current=true }
  },[running,animId])
  return <canvas ref={ref} style={CS}/>
}

const CS = { width:"100%", height:"auto", display:"block", borderRadius:"6px", border:"1px solid rgba(0,255,120,0.12)" }

export default function App() {
  const [imgId,setImgId]=useState(IMAGES[0].id)
  const [pixels,setPixels]=useState(null)
  const [loading,setLoading]=useState(false)
  const [animId,setAnimId]=useState(ANIMS[0].id)
  const [running,setRunning]=useState(false)

  async function handleGenerer() {
    setLoading(true); setPixels(null)
    try {
      const res=await fetch(`${API}/dessiner/${imgId}`)
      const data=await res.json()
      if (data.pixels) setPixels(data.pixels)
      else alert("Erreur Python : "+(data.erreur??"?"))
    } catch { alert("Backend Flask introuvable.\nLance : python app.py") }
    finally { setLoading(false) }
  }

  const animLabel=ANIMS.find(a=>a.id===animId)?.label??""

  return (
    <div style={{minHeight:"100vh",background:"#070a0f",color:"#c8ffd0",fontFamily:"'Courier New',monospace",display:"flex",flexDirection:"column"}}>
      <header style={{display:"flex",alignItems:"center",justifyContent:"center",gap:"16px",padding:"16px 0 13px",borderBottom:"1px solid rgba(0,200,80,0.18)"}}>
        <span style={{color:"#00ff88",opacity:.5}}>█</span>
        <span style={{fontSize:"15px",fontWeight:700,color:"#00ff88",letterSpacing:".3em",textShadow:"0 0 22px rgba(0,255,136,.45)"}}>PIXEL ART STUDIO</span>
        <span style={{color:"#00ff88",opacity:.5}}>█</span>
      </header>

      <div style={{display:"grid",gridTemplateColumns:"1fr 1px 1fr",flex:1}}>

        {/* IMAGES */}
        <section style={{padding:"22px 26px 20px",display:"flex",flexDirection:"column",gap:"13px"}}>
          <div style={{display:"flex",alignItems:"center",gap:"9px"}}>
            <span style={{fontSize:"9px",fontWeight:700,padding:"2px 8px",borderRadius:"3px",border:"1px solid rgba(255,200,0,.35)",background:"rgba(255,200,0,.1)",color:"#ffd040",letterSpacing:".08em"}}>IMG</span>
            <h2 style={{fontSize:"12px",fontWeight:700,color:"#e8ffe8",margin:0}}>Générateur d'images</h2>
          </div>
          <p style={{fontSize:"10px",color:"rgba(0,200,80,.45)",fontStyle:"italic"}}>
            → appelle <code style={{fontStyle:"normal",color:"rgba(0,220,120,.8)"}}>Dessiner("{imgId}")</code> dans dessin.py
          </p>
          <div style={{display:"flex",gap:"8px"}}>
            <div style={{flex:1,position:"relative"}}>
              <select style={{width:"100%",padding:"8px 30px 8px 10px",background:"rgba(0,255,100,.04)",border:"1px solid rgba(0,200,80,.25)",borderRadius:"4px",color:"#a0ffc0",fontSize:"11px",fontFamily:"'Courier New',monospace",cursor:"pointer",appearance:"none",outline:"none"}}
                value={imgId} onChange={e=>{setImgId(e.target.value);setPixels(null)}}>
                {IMAGES.map(i=><option key={i.id} value={i.id}>{i.label}</option>)}
              </select>
              <span style={{position:"absolute",right:"9px",top:"50%",transform:"translateY(-50%)",pointerEvents:"none",color:"rgba(0,200,80,.5)"}}>▾</span>
            </div>
            <button style={{padding:"8px 15px",border:"1px solid rgba(255,200,0,.4)",borderRadius:"4px",fontSize:"11px",fontFamily:"'Courier New',monospace",fontWeight:700,cursor:"pointer",background:"rgba(255,200,0,.1)",color:"#ffd040"}}
              onClick={handleGenerer} disabled={loading}>
              {loading?"Python…":"GÉNÉRER"}
            </button>
          </div>
          <div style={{background:"#080b10",borderRadius:"6px",overflow:"hidden",border:"1px solid rgba(0,255,120,.1)",flex:1}}>
            <ImageCanvas pixels={pixels}/>
          </div>
        </section>

        <div style={{background:"rgba(0,200,80,0.12)"}}/>

        {/* ANIMATIONS */}
        <section style={{padding:"22px 26px 20px",display:"flex",flexDirection:"column",gap:"13px"}}>
          <div style={{display:"flex",alignItems:"center",gap:"9px"}}>
            <span style={{fontSize:"9px",fontWeight:700,padding:"2px 8px",borderRadius:"3px",border:"1px solid rgba(0,220,120,.3)",background:"rgba(0,220,120,.1)",color:"#00dc78",letterSpacing:".08em"}}>ANIM</span>
            <h2 style={{fontSize:"12px",fontWeight:700,color:"#e8ffe8",margin:0}}>Générateur d'animations</h2>
          </div>
          <p style={{fontSize:"10px",color:"rgba(0,200,80,.45)",fontStyle:"italic"}}>
            → appelle <code style={{fontStyle:"normal",color:"rgba(0,220,120,.8)"}}>Animer("{animId}", frame)</code> dans animation.py
          </p>
          <div style={{display:"flex",gap:"8px"}}>
            <div style={{flex:1,position:"relative"}}>
              <select style={{width:"100%",padding:"8px 30px 8px 10px",background:"rgba(0,255,100,.04)",border:"1px solid rgba(0,200,80,.25)",borderRadius:"4px",color:"#a0ffc0",fontSize:"11px",fontFamily:"'Courier New',monospace",cursor:"pointer",appearance:"none",outline:"none"}}
                value={animId} onChange={e=>{setRunning(false);setAnimId(e.target.value)}}>
                {ANIMS.map(a=><option key={a.id} value={a.id}>{a.label}</option>)}
              </select>
              <span style={{position:"absolute",right:"9px",top:"50%",transform:"translateY(-50%)",pointerEvents:"none",color:"rgba(0,200,80,.5)"}}>▾</span>
            </div>
            <button style={{padding:"8px 15px",border:"1px solid",borderRadius:"4px",fontSize:"11px",fontFamily:"'Courier New',monospace",fontWeight:700,cursor:"pointer",
              ...(running?{background:"rgba(220,50,50,.13)",color:"#ff6060",borderColor:"rgba(220,50,50,.4)"}:{background:"rgba(0,220,100,.1)",color:"#00dc64",borderColor:"rgba(0,220,100,.4)"})}}
              onClick={()=>setRunning(r=>!r)}>
              {running?"⏹ STOP":"▶ PLAY"}
            </button>
          </div>
          <div style={{background:"#080b10",borderRadius:"6px",overflow:"hidden",border:"1px solid rgba(0,255,120,.1)",flex:1}}>
            <AnimCanvas animId={animId} running={running}/>
          </div>
          {running&&(
            <div style={{display:"flex",alignItems:"center",gap:"8px",padding:"5px 9px",background:"rgba(0,220,100,.05)",border:"1px solid rgba(0,220,100,.14)",borderRadius:"4px"}}>
              <span style={{width:"6px",height:"6px",borderRadius:"50%",background:"#00dc64",boxShadow:"0 0 7px #00dc64",flexShrink:0,display:"inline-block"}}/>
              <span style={{fontSize:"9px",color:"rgba(0,220,100,.65)",letterSpacing:".1em"}}>EN COURS · {animLabel.trim()}</span>
            </div>
          )}
        </section>

      </div>

      <footer style={{textAlign:"center",padding:"9px",fontSize:"9px",color:"rgba(0,200,80,.2)",borderTop:"1px solid rgba(0,200,80,.08)",letterSpacing:".1em"}}>
        dessin.py · animation.py · flask api → json → canvas · {COLS}×{ROWS}
      </footer>
    </div>
  )
}
