"""Usa rasterize de render_docx.py con conversión Word nativa en Windows.

El renderer empaquetado falló por ausencia de LibreOffice. Solo se sustituye
convert_to_pdf, sin alterar la habilidad instalada. Abre DOCX en solo lectura.
"""
from pathlib import Path
import importlib.util, os, sys
import win32com.client

def run(docx, target, skill, poppler):
    os.environ['PATH']=str(poppler)+os.pathsep+os.environ['PATH']
    spec=importlib.util.spec_from_file_location('document_renderer',str(Path(skill)/'render_docx.py'))
    renderer=importlib.util.module_from_spec(spec);spec.loader.exec_module(renderer)
    def word_pdf(doc_path, user_profile, convert_tmp_dir, stem, verbose=False):
        app=win32com.client.DispatchEx('Word.Application');app.Visible=False;app.DisplayAlerts=0
        doc=None
        try:
            doc=app.Documents.Open(str(Path(doc_path).resolve()),ReadOnly=True,AddToRecentFiles=False)
            doc.Fields.Update();doc.Repaginate()
            pdf=str(Path(convert_tmp_dir)/f'{stem}.pdf');doc.ExportAsFixedFormat(pdf,17)
            print('WORD_PAGES',doc.ComputeStatistics(2))
            return pdf,'Microsoft Word COM; fallback documentado tras falta de soffice.exe'
        finally:
            if doc is not None:doc.Close(False)
            app.Quit()
    renderer.convert_to_pdf=word_pdf
    print(renderer.rasterize(str(docx),str(target),130,False,True))

if __name__=='__main__':run(*sys.argv[1:])
