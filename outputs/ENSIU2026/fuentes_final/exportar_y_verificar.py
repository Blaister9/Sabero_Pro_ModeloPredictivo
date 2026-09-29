"""Exporta el PPTX final con PowerPoint y verifica conservación. No ejecuta modelos.
Ejecutar desde la raíz del worktree con el Python que incluye pywin32, fitz y PIL.
"""
from pathlib import Path
from zipfile import ZipFile
from lxml import etree
import hashlib, json, re, unicodedata
import fitz
import win32com.client
from PIL import Image, ImageChops, ImageStat

ROOT=Path.cwd()
BUILD=ROOT/'build/ensiu2026'
OUT=ROOT/'outputs/ENSIU2026'
SOURCE=ROOT/'outputs/CONACIC2026/PRESENTACION_CONACIC2026_FINAL.pptx'
FINAL=OUT/'PRESENTACION_ENSIU2026_FINAL.pptx'
PDF=OUT/'PRESENTACION_ENSIU2026_FINAL.pdf'
NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def shape_text(shape):
    return '\n'.join(''.join(p.itertext()) for p in shape.findall('.//a:p',NS))
def slide_shapes(archive,n):
    return list(etree.fromstring(archive.read(f'ppt/slides/slide{n}.xml')).find('p:cSld/p:spTree',NS))[2:]

assert FINAL.exists()
checks={'slides':[], 'originals_intact':False}
old=json.loads((OUT/'fuentes_final/ORIGINALES_SHA256.json').read_text(encoding='utf-8'))
changed=[p for p,h in old.items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h]
assert not changed,changed
checks['originals_intact']=True
checks['protected_original_count']=len(old)
with ZipFile(SOURCE) as a,ZipFile(FINAL) as b:
    forbidden=[]
    for f in b.namelist():
        if f.endswith(('.xml','.rels')):
            text=b.read(f).decode('utf-8')
            plain=''.join(etree.fromstring(b.read(f)).itertext())
            normalized=unicodedata.normalize('NFKD',text+' '+plain)
            if re.search(r'CONACIC|UADY|SIMULTA.NEA|SIMULTANEA|SIMCISE',normalized,re.I):forbidden.append(f)
    assert not forbidden,forbidden
    checks['old_identity_absent_xml']=True
    preserved=[f for f in a.namelist() if f.startswith(('ppt/charts/','ppt/embeddings/')) or f in ['ppt/media/image1.png','ppt/media/image5.png','ppt/media/image6.png','ppt/media/image7.png']]
    assert all(a.read(f)==b.read(f) for f in preserved)
    checks['unchanged_scientific_parts']=preserved
    checks['removed_brand_media']=[f for f in ['ppt/media/image2.emf','ppt/media/image3.png','ppt/media/image4.png'] if f not in b.namelist()]
    assert len(checks['removed_brand_media'])==3
    for n in range(1,11):
        before,after=slide_shapes(a,n),slide_shapes(b,n)
        assert len(before)==len(after)
        changed_shapes=[]
        for i,(x,y) in enumerate(zip(before,after)):
            # El pie es la única variación admisible en las siete slides científicas.
            xx=etree.tostring(x).replace(b'CONACIC 2026',b'ENSIU 2026')
            yy=etree.tostring(y)
            if xx!=yy:changed_shapes.append(i)
        expected={1:[3,6],2:[9],10:[10]}.get(n,[])
        assert changed_shapes==expected,(n,changed_shapes,expected)
        checks['slides'].append({'slide':n,'content_shape_changes':changed_shapes,'same_object_count':True,'content_unchanged_except_footer':not changed_shapes})
    tablea=etree.fromstring(a.read('ppt/slides/slide7.xml')).find('.//a:tbl',NS)
    tableb=etree.fromstring(b.read('ppt/slides/slide7.xml')).find('.//a:tbl',NS)
    assert etree.tostring(tablea)==etree.tostring(tableb)
    checks['table_byte_identical']=True

app=win32com.client.DispatchEx('PowerPoint.Application')
app.DisplayAlerts=1
checks['powerpoint_version']=app.Version
geometry=[]
try:
    for tag,file in [('original',SOURCE),('final',FINAL)]:
        deck=app.Presentations.Open(str(file),True,False,False)
        try:
            assert deck.Slides.Count==10
            render=BUILD/f'render_{tag}';render.mkdir(exist_ok=True)
            for slide in deck.Slides:
                slide.Export(str(render/f'slide_{slide.SlideIndex:02}.png'),'PNG',1920,1080)
                if tag=='final':
                    for shape in slide.Shapes:
                        if shape.HasTextFrame and shape.TextFrame.HasText:
                            tf=shape.TextFrame2;tr=tf.TextRange
                            geometry.append(dict(slide=slide.SlideIndex,name=shape.Name,text=shape.TextFrame.TextRange.Text,
                                left=shape.Left,top=shape.Top,width=shape.Width,height=shape.Height,
                                text_bound=[tr.BoundLeft,tr.BoundTop,tr.BoundWidth,tr.BoundHeight]))
            if tag=='final':deck.SaveAs(str(PDF),32)
        finally:deck.Close()
finally:app.Quit()

doc=fitz.open(PDF)
assert len(doc)==10
pdftext='\n'.join(p.get_text() for p in doc)
assert not re.search(r'CONACIC|UADY|SIMULTÁNEA|SIMULTANEA|SIMCISE',pdftext,re.I)
for text in ['127.716','98.954','28.762','9,33','6,21','0,706','10,2294','10,0722','16,8588','Sucre','Chocó','Putumayo','Nathalia Orozco Morales','1071010']:
    assert text in pdftext,text
pdf_renders=BUILD/'render_pdf';pdf_renders.mkdir(exist_ok=True)
for n,p in enumerate(doc,1):p.get_pixmap(matrix=fitz.Matrix(2,2)).save(pdf_renders/f'slide_{n:02}.png')
checks['pdf_pages']=len(doc)
checks['expected_figures_and_names_in_pdf']=True
checks['sha256_pptx']=sha(FINAL);checks['sha256_pdf']=sha(PDF)
checks['pixel_comparisons']=[]
for n in [3,4,5,6,7,8,9]:
    # Región de contenido exacta (PowerPoint, 1920x1080). Excluye logos y pies.
    crop=(135,220,1808,964)
    x=Image.open(BUILD/f'render_original/slide_{n:02}.png').convert('RGB').crop(crop)
    y=Image.open(BUILD/f'render_final/slide_{n:02}.png').convert('RGB').crop(crop)
    identical=ImageChops.difference(x,y).getbbox() is None
    checks['pixel_comparisons'].append({'slide':n,'body_pixel_identical':identical})
    assert identical,n
checks['pdf_pptx_render_equivalence']=[]
for n in range(1,11):
    aimg=Image.open(BUILD/f'render_final/slide_{n:02}.png').convert('RGB')
    bimg=Image.open(BUILD/f'render_pdf/slide_{n:02}.png').convert('RGB').resize(aimg.size,Image.Resampling.LANCZOS)
    diff=ImageChops.difference(aimg,bimg)
    checks['pdf_pptx_render_equivalence'].append({'slide':n,'mean_channel_difference_0_255':round(sum(ImageStat.Stat(diff).mean)/3,4)})

(BUILD/'text_geometry.json').write_text(json.dumps(geometry,ensure_ascii=False,indent=2),encoding='utf-8')
(BUILD/'verificacion.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(BUILD/'final_pdf_text.txt').write_text(pdftext,encoding='utf-8')
print(json.dumps(checks,ensure_ascii=False,indent=2))
