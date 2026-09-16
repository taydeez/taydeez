from pathlib import Path
from html import escape
import shutil, re, xml.etree.ElementTree as ET
from zipfile import ZipFile, ZIP_DEFLATED

R=Path(__file__).parent
(R/'assets').mkdir(exist_ok=True)

class Panel:
 def __init__(self,h,title,dark):
  self.ink='#e8e7e2' if dark else '#20272a'; self.muted='#9ca9ae' if dark else '#526268'; self.line='#36454d' if dark else '#c4cdc9'; self.accent='#ff946f' if dark else '#ae4528'; self.bg='#0d1117' if dark else '#ffffff'
  self.s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 {h}" role="img" aria-label="{escape(title)}"><title>{escape(title)}</title><style>text{{font-family:Consolas,monospace}}.packet{{stroke-dasharray:6 30;animation:flow 4s linear infinite}}@keyframes flow{{to{{stroke-dashoffset:-144}}}}.pulse{{animation:pulse 3s ease-in-out infinite}}@keyframes pulse{{50%{{opacity:.35}}}}@media(prefers-reduced-motion:reduce){{.packet,.pulse{{animation:none}}}}</style><rect width="1000" height="{h}" fill="{self.bg}"/>']
 def text(self,x,y,s,n=20,c=None,anchor='start',family=None):
  style=f' style="font-family:{family}"' if family else ''
  self.s.append(f'<text x="{x}" y="{y}" font-size="{n}" fill="{c or self.ink}" text-anchor="{anchor}"{style}>{escape(s)}</text>')
 def line_at(self,x,y,x2,y2,c=None): self.s.append(f'<path d="M{x} {y}L{x2} {y2}" fill="none" stroke="{c or self.line}"/>')
 def path(self,path,c=None,cls=''): self.s.append(f'<path d="{path}" fill="none" stroke="{c or self.line}" stroke-width="1.5" class="{cls}"/>')
 def rect(self,x,y,w,h,c=None): self.s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{self.bg}" stroke="{c or self.line}"/>')
 def dot(self,x,y,r=4,c=None,cls=''): self.s.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c or self.accent}" class="{cls}"/>')
 def chapter(self,num,name,route):
  self.text(36,56,num,42,self.accent); self.text(112,50,name.upper(),19); self.line_at(112,70,964,70); self.text(964,49,route,14,self.muted,'end')
 def lines(self,x,y,lines,n=21):
  for i,s in enumerate(lines): self.text(x,y+i*32,s,n,self.muted)
 def save(self,name,dark):
  target=R/'assets'/('dark' if dark else 'light'); target.mkdir(exist_ok=True)
  out=''.join(self.s)+'</svg>'; ET.fromstring(out); (target/(name+'.svg')).write_text(out,encoding='utf-8')

for dark in [False,True]:
 p=Panel(378,'About Demilade Oyewusi',dark); p.chapter('01','The engineer','~/demilade')
 p.text(36,126,'People see the product.',34,family='Georgia,serif'); p.text(36,173,'I think about what holds it together.',34,family='Georgia,serif')
 p.lines(36,224,['8+ years building commerce, MultiTenant SaaS, financial and data platforms.'])
 p.line_at(36,285,964,285)
 for x,big,small in [(36,'BACKEND FIRST','Laravel · .NET · Node.js'),(370,'AI IN THE WORKFLOW','OpenAI Codex · Claude'),(735,'OPEN TO REMOTE','Nigeria / worldwide')]:
  p.text(x,322,big,17,p.accent); p.text(x,354,small,16,p.muted)
 p.save('about',dark)

 p=Panel(584,'Illustrative backend request flow; not live system telemetry',dark); p.chapter('02','Under the hood','~/request-flow')
 p.text(36,116,'A request is only the beginning.',32,family='Georgia,serif'); p.text(36,153,'ILLUSTRATIVE FLOW / PATTERNS I WORK WITH',15,p.muted)
 # Connection routes sit behind the boxes. Animated dashes represent data flow.
 paths=['M220 262H326','M588 262H700','M457 310V413H700','M820 310V365H900V413']
 for path in paths: p.path(path); p.path(path,p.accent,'packet')
 nodes=[(36,215,184,94,'CLIENT','Web / storefront'),(326,215,262,94,'APPLICATION','Validate · authorize'),(700,215,264,94,'TRANSACTION','State + outbox event'),(700,413,264,94,'BACKGROUND JOB','Queue → consumer')]
 for x,y,w,h,a,b in nodes:
  p.rect(x,y,w,h,p.accent if a=='APPLICATION' else None); p.text(x+18,y+36,a,20); p.text(x+18,y+68,b,16,p.muted)
 p.text(267,241,'API',14,p.muted,'middle'); p.text(644,241,'WRITE',14,p.muted,'middle'); p.text(487,394,'async work',15,p.muted)
 p.lines(36,387,['Idempotent payments.', 'Consistent transactions.', 'Events delivered asynchronously.'],21)
 p.line_at(36,541,964,541); p.text(36,571,'PATTERNS: TRANSACTIONS / OUTBOX / QUEUES / IDEMPOTENCY',16,p.accent)
 p.save('flow',dark)

 p=Panel(658,'Selected engineering work',dark); p.chapter('03','Systems I have worked on','~/selected-work')
 entries=[('01','GLAMRUSH','Commerce + conversational AI',['Multi-storefront commerce with Paystack and Flutterwave.', 'Idempotent payments, outbox events and an AI / LLM chatbot.'],'Laravel / Nuxt / PostgreSQL / Redis'),('02','RB2','Loyalty for a national audience',['Contributed to Club Staatsloterij, the Dutch National', 'Lottery loyalty platform, with a distributed engineering team.'],'C# / .NET / CQRS / MSSQL / Azure'),('03','CITITRUST','Accounting with a traceable history',['Led three engineers on accounting and financial workflows.', 'Immutable records, role-based access and detailed audit trails.'],'PHP / Transactions / Auditability')]
 for i,(num,org,title,lines,stack) in enumerate(entries):
  y=113+i*178; p.text(36,y,num,17,p.accent); p.text(87,y,org,17,p.muted); p.text(87,y+38,title,29,family='Georgia,serif'); p.lines(87,y+74,lines,18); p.text(87,y+134,stack,15,p.accent); p.line_at(36,y+155,964,y+155)
 p.save('work',dark)

 p=Panel(581,'Career timeline, May 2017 through July 2026',dark); p.chapter('04','The route here','~/experience')
 jobs=[('2017–2018','PayPorte','Magento / commerce & payment integrations'),('2018–2019','Cititrust','Accounting / team leadership & data integrity'),('2019–2020','Terragon','Data platforms / APIs & Kafka pipelines'),('2020–2025','rb2','Netherlands · remote / loyalty & commerce'),('2025–2026','Glamrush','Contract / commerce, payments & AI chatbot')]
 p.line_at(221,129,221,488,p.accent)
 for i,(date,org,detail) in enumerate(jobs):
  y=134+i*87; p.text(36,y,date,18,p.muted); p.dot(221,y-5); p.text(255,y,org,26); p.text(255,y+29,detail,18,p.muted)
 p.text(36,552,'MAY 2017 → JUL 2026   /   BUILDING ACROSS DOMAINS',16,p.accent); p.save('route',dark)

 p=Panel(555,'Backend engineering toolkit and AI workflow',dark); p.chapter('05','The working set','~/stack')
 rows=[('01 / BUILD','PHP · Laravel · C# · .NET','Node.js · TypeScript · REST APIs'),('02 / DATA','PostgreSQL · MySQL · MSSQL','Redis · Transactions · Caching'),('03 / CONNECT','Kafka · RabbitMQ · Laravel Queues','CQRS · Transactional outbox'),('04 / DELIVER','Docker · CI/CD · Azure','Google Cloud · Vue.js · Nuxt')]
 for i,(name,one,two) in enumerate(rows):
  y=119+i*86; p.text(36,y,name,16,p.accent); p.text(260,y,one,21); p.text(260,y+30,two,19,p.muted); p.line_at(36,y+50,964,y+50)
 p.rect(36,460,928,68,p.accent); p.dot(59,494,4,cls='pulse'); p.text(80,500,'AI WORKFLOW',17,p.accent); p.text(293,500,'OpenAI Codex + Claude · LLM integration',20); p.save('stack',dark)

 p=Panel(224,'Contact Demilade; open to remote opportunities worldwide',dark); p.chapter('06','Start a conversation','~/connect')
 p.text(36,128,'Let’s build something dependable.',33,family='Georgia,serif'); p.text(36,182,'demioyewusi@gmail.com',23,p.accent); p.text(964,182,'OPEN TO REMOTE',17,p.muted,'end'); p.save('contact',dark)

alts={'about':'Demilade: 8+ years of backend engineering, Laravel, .NET, Node.js. Codex and Claude in the development workflow.','flow':'Animated conceptual request flow: client to application to transaction and outbox, then queue consumer. Illustrative, not live telemetry.','work':'Glamrush: commerce, payments and AI chatbot. rb2: Dutch National Lottery loyalty. Cititrust: accounting, audit trails and team leadership.','route':'Career: PayPorte 2017–2018; Cititrust 2018–2019; Terragon 2019–2020; rb2 2020–2025; Glamrush 2025–2026.','stack':'PHP, Laravel, C#, .NET, Node.js, TypeScript, PostgreSQL, MySQL, MSSQL, Redis, Kafka, RabbitMQ, Docker, Azure, Google Cloud, Vue and Nuxt. AI: Codex, Claude and LLM integration.','contact':'Contact demioyewusi@gmail.com. Open to remote opportunities worldwide.'}
def picture(name): return f'<picture><source media="(prefers-color-scheme: dark)" srcset="assets/dark/{name}.svg" /><img src="assets/light/{name}.svg" width="100%" alt="{escape(alts[name],quote=True)}" /></picture>'
nav='<p align="center"><a href="https://www.linkedin.com/in/demilade-oyewusi/">LINKEDIN ↗</a> &nbsp; / &nbsp; <a href="mailto:demioyewusi@gmail.com">EMAIL ↗</a> &nbsp; / &nbsp; <a href="https://github.com/taydeez?tab=repositories">REPOSITORIES ↗</a></p>'
parts=['<p><code>D/O — ENGINEERING INDEX</code></p><h1>Demilade Oyewusi</h1><p><strong>Senior Backend Engineer</strong> · Nigeria / Remote</p><p>Reliable systems. Thoughtful architecture.</p>',nav]
parts += [picture(n) for n in ['about','flow','work']]
parts += ['<p><strong>On GitHub:</strong> <a href="https://github.com/taydeez/SELL_SPREE_BE">Sell Spree ↗</a> — a backend service for a digital marketplace.</p>']
parts += [picture(n) for n in ['route','stack']]
parts += ['''<details><summary><strong>Read the profile as text</strong></summary>

I'm Demilade Oyewusi, a Senior Backend Engineer with 8+ years of experience building production systems across commerce, financial operations, loyalty and data platforms.

- **Glamrush (Dec 2025–Jul 2026):** Multi-storefront e-commerce, Paystack and Flutterwave payments, idempotent workflows, transactional outbox events, and an AI/LLM customer service chatbot.
- **rb2 (Jul 2020–May 2025):** Contributed to Club Staatsloterij, the Dutch National Lottery loyalty platform, using C#/.NET, CQRS, MSSQL and Azure.
- **Terragon (May 2019–May 2020):** Backend services and Kafka pipelines for data ingestion, synchronization and processing.
- **Cititrust (Nov 2018–Apr 2019):** Led three engineers building accounting workflows with immutable records, access controls and audit trails.
- **PayPorte (May 2017–Nov 2018):** Magento commerce, payments, checkout, shipping and installment payment functionality.

**Tools:** PHP, Laravel, C#, .NET, Node.js, TypeScript, PostgreSQL, MySQL, MSSQL, Redis, Kafka, RabbitMQ, Laravel Queues, Docker, CI/CD, Azure, Google Cloud, Vue.js and Nuxt.

**AI:** OpenAI Codex and Claude in my daily development workflow, plus AI/LLM integration for customer service.

**Concept diagram:** A client request is validated and authorized by an application; a transaction persists state and an outbox event; queued work runs asynchronously. The diagram illustrates familiar patterns rather than a specific production deployment.

Based in Nigeria and open to remote opportunities worldwide.

</details>''']
parts += [f'<a href="mailto:demioyewusi@gmail.com">{picture("contact")}</a>']
(R/'README.md').write_text('\n\n'.join(parts)+'\n',encoding='utf-8')
previewparts=parts.copy(); previewparts[-2]='<details><summary>Read the profile as text</summary><p>Backend engineering across commerce, finance, loyalty and data platforms. Full accessible profile text is included in README.md.</p></details>'
css='''*{box-sizing:border-box}body{background:#fff;color:#20272a;font:16px/1.6 Consolas,monospace;margin:0}main{max-width:1000px;margin:28px auto;padding:24px;border:1px solid #c4cdc9;border-radius:6px}img{width:100%;display:block}picture{display:block}p,details{margin:24px 12px}a{color:#ae4528}summary{cursor:pointer}#controls{display:flex;justify-content:center;gap:14px;padding:10px}button{font:inherit;padding:8px 16px;background:none;color:inherit;border:1px solid #8b949e;cursor:pointer}@media(prefers-color-scheme:dark){body{background:#0d1117;color:#e8e7e2}main{border-color:#36454d}a{color:#ff946f}}@media(max-width:600px){main{margin:0;padding:8px;border:0}p,details{font-size:13px}}'''
script='''function theme(dark){document.body.style.background=dark?'#0d1117':'#fff';document.body.style.color=dark?'#e8e7e2':'#20272a';document.querySelectorAll('picture').forEach(p=>{p.querySelector('source').media=dark?'all':'not all'});document.querySelectorAll('a').forEach(a=>a.style.color=dark?'#ff946f':'#ae4528')}'''
(R/'preview.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Demilade / Profile preview</title><style>'+css+'</style></head><body><div id="controls"><button onclick="theme(false)">Light preview</button><button onclick="theme(true)">Dark preview</button></div><main>'+''.join(previewparts)+'</main><script>'+script+'</script></body></html>',encoding='utf-8')
(R/'SETUP.md').write_text('''# Install your profile

1. Extract this ZIP. Open preview.html to inspect the layout, with light/dark preview buttons.
2. Sign in to GitHub as taydeez. Create a PUBLIC repository named taydeez, or open taydeez/taydeez if it exists.
3. Upload README.md and the entire assets folder to the repository root. Keep the dark and light subfolders intact. Commit the files.
4. Visit https://github.com/taydeez. GitHub automatically displays that repository's README.

Only README.md and assets are required for GitHub. No workflow, credentials, package install or hosted widget is required.

There is no portrait or banner. The introduction is ordinary HTML text and the numbered panels are original SVGs generated by build.py. The README selects light/dark variants using picture sources. The request diagram contains CSS animation and respects reduced-motion preferences. It is an illustration, not live telemetry. A readable text version sits in a collapsible section for accessibility and small screens.

The local preview approximates GitHub rendering; final outer spacing is controlled by GitHub. Preview buttons are local only. On GitHub the variants follow the browser/device color preference.

To revise the panels, edit their SVG text directly. To revise the introduction, edit README.md.

Design reference: https://github.com/Sharann-del — inspiration for numbered chapters, technical diagrams and theme variants. No source artwork was copied.
GitHub setup: https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme
''',encoding='utf-8')
for match in re.findall(r'(?:src|srcset)="([^"]+)"',(R/'README.md').read_text(encoding='utf-8')): assert (R/match).is_file(),match
with ZipFile(R.parent/'taydeez-github-profile-v3.zip','w',ZIP_DEFLATED) as z:
 for name in ['README.md','SETUP.md','preview.html']: z.write(R/name,name)
 for path in (R/'assets').rglob('*.svg'):
  if path.is_file(): z.write(path,path.relative_to(R))
print('Built 12 theme panels; checked XML and image paths; packaged profile v3.')
