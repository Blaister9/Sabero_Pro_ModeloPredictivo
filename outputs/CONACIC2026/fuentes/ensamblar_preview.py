"""Montaje local PREVIEW por diapositiva y audio reemplazable. Sin publicación."""
from pathlib import Path
import argparse, json, math, shutil, struct, subprocess, tempfile, wave

OUT=Path(__file__).resolve().parents[1]

def execute(args):
    subprocess.run([str(x) for x in args],check=True)

def probe(file):
    p=subprocess.run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(file)],check=True,capture_output=True,text=True)
    return json.loads(p.stdout)

def audio_duration(file):
    d=probe(file)
    if not any(s['codec_type']=='audio' for s in d['streams']):raise ValueError(f'Sin pista de audio: {file}')
    return float(d['format']['duration'])

def segment(frame,audio,seconds,dest):
    # All paths are subprocess argument list elements; never shell interpolation.
    font=Path('C:/Windows/Fonts/arial.ttf')
    font_opt=''
    if font.exists():font_opt="fontfile='"+font.as_posix().replace(':',r'\:')+"':"
    vf='scale=1920:1080:force_original_aspect_ratio=decrease:out_range=tv,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p,'
    vf+='drawtext='+font_opt+'text=PREVIEW:x=w-tw-40:y=30:fontsize=36:fontcolor=yellow:box=1:boxcolor=black@0.6'
    execute(['ffmpeg','-hide_banner','-loglevel','error','-n','-loop','1','-framerate','30','-i',frame,'-i',audio,'-vf',vf,'-af','loudnorm=I=-16:TP=-1.5:LRA=11,apad','-t',f'{seconds:.3f}','-r','30','-c:v','libx264','-preset','medium','-tune','stillimage','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-movflags','+faststart',dest])

def validate(file,expected):
    d=probe(file);v=next(s for s in d['streams'] if s['codec_type']=='video');a=next(s for s in d['streams'] if s['codec_type']=='audio');duration=float(d['format']['duration'])
    assert (v['width'],v['height'])==(1920,1080)
    assert v['codec_name']=='h264' and v['pix_fmt']=='yuv420p' and a['codec_name']=='aac'
    assert duration<=600 and abs(duration-expected)<1
    report={'status':'PREVIEW','duration_seconds':duration,'expected_seconds':expected,'video':v['codec_name'],'width':v['width'],'height':v['height'],'pixel_format':v['pix_fmt'],'frame_rate':v['avg_frame_rate'],'audio':a['codec_name'],'sample_rate':a['sample_rate'],'path':str(file)}
    file.with_suffix('.verificacion.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--audio-dir',type=Path,default=OUT/'audio/voz_real');ap.add_argument('--output',type=Path,default=OUT/'PREVIEW_RITMO.mp4');ap.add_argument('--check',action='store_true');ap.add_argument('--dry-run',action='store_true');ap.add_argument('--smoke-test',action='store_true');args=ap.parse_args()
    for binary in ['ffmpeg','ffprobe']:
        if not shutil.which(binary):raise SystemExit(f'Falta {binary} en PATH')
    config=json.loads((OUT/'CRONOMETRAJE.json').read_text(encoding='utf-8'));slides=config['slides']
    assert len(slides)==10 and sum(s['seconds'] for s in slides)==510
    for s in slides:
        if not (OUT/f'escenas/{s["slide"]:02d}.jpg').is_file():raise SystemExit(f'Falta escena {s["slide"]}')
    if args.check:
        print('OK: 10 escenas, guion y 510 segundos planificados. Audios reales pendientes de grabación.');return
    output=args.output.resolve()
    if not output.name.upper().startswith('PREVIEW') or output.suffix.lower()!='.mp4':raise SystemExit('Esta fase solo admite salida PREVIEW*.mp4')
    if output.exists():raise SystemExit('La salida ya existe. Elija otro nombre para conservarla.')
    output.parent.mkdir(parents=True,exist_ok=True)
    if args.smoke_test:
        with tempfile.TemporaryDirectory(prefix='conacic_control_') as scratch:
            wav=Path(scratch)/'control.wav'
            with wave.open(str(wav),'wb') as w:
                w.setnchannels(1);w.setsampwidth(2);w.setframerate(48000)
                w.writeframes(b''.join(struct.pack('<h',int(800*math.sin(2*math.pi*440*i/48000))) for i in range(48000)))
            segment(OUT/'escenas/01.jpg',wav,2,output)
        validate(output,2);return
    plan=[]
    for s in slides:
        audio=(args.audio_dir/f'{s["slide"]:02d}.wav').resolve()
        if not audio.is_file():raise SystemExit(f'Falta audio real o preliminar: {audio}')
        seconds=max(s['seconds'],math.ceil((audio_duration(audio)+0.5)*30)/30)
        plan.append({'slide':s['slide'],'audio':str(audio),'seconds':seconds})
    total=sum(s['seconds'] for s in plan)
    if total>600:raise SystemExit(f'El montaje excede 10 minutos: {total:.2f} segundos. Revisar narración.')
    print(json.dumps({'status':'PREVIEW','total_seconds':total,'plan':plan},indent=2))
    if args.dry_run:return
    with tempfile.TemporaryDirectory(prefix='conacic_preview_') as scratch:
        scratch=Path(scratch);clips=[]
        for s in plan:
            clip=scratch/f'{s["slide"]:02d}.mp4';segment(OUT/f'escenas/{s["slide"]:02d}.jpg',s['audio'],s['seconds'],clip);clips.append(clip)
        listing=scratch/'concat.txt'
        listing.write_text('\n'.join("file '"+p.as_posix().replace("'","'\\''")+"'" for p in clips),encoding='utf-8')
        execute(['ffmpeg','-hide_banner','-loglevel','error','-n','-f','concat','-safe','0','-i',listing,'-c','copy','-movflags','+faststart',output])
    validate(output,total)

if __name__=='__main__':main()
