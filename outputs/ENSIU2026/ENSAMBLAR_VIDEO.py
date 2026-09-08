"""Monta únicamente esta entrega ENSIU desde sus ocho escenas y voz ya generadas."""
from pathlib import Path
import json, shutil, subprocess, sys

base=Path(__file__).resolve().parent
ffmpeg=shutil.which('ffmpeg') or 'C:/ffmpeg/bin/ffmpeg.exe'
ffprobe=shutil.which('ffprobe') or 'C:/ffmpeg/bin/ffprobe.exe'
timing=json.loads((base/'CRONOMETRAJE.json').read_text(encoding='utf-8'))
scenes=timing['scenes']
assert len(scenes)==8 and scenes[0]['start']==0 and scenes[-1]['end']==60
args=[ffmpeg,'-y','-hide_banner','-loglevel','warning','-filter_complex_threads','2']
filters=[]
for i,s in enumerate(scenes):
    duration=s['end']-s['start']+(0.3 if i<7 else 0)
    args+=['-loop','1','-framerate','30','-t',f'{duration:.6f}','-i',str(base/'escenas'/f'escena_{i+1:02d}.png')]
    filters.append(f'[{i}:v]fps=30,format=yuv444p,settb=AVTB,setpts=PTS-STARTPTS[v{i}]')
args+=['-i',str(base/'audio/VOZ_ENSIU_60s.wav'),'-i',str(base/'SUBTITULOS_ENSIU.srt')]
last='v0'
for i in range(1,8):
    label=f'mix{i}'
    filters.append(f'[{last}][v{i}]xfade=transition=fade:duration=0.3:offset={scenes[i]["start"]:.6f}[{label}]')
    last=label
filters.append(f'[{last}]fps=30,format=yuv420p[vfinal]')
args+=['-filter_complex',';'.join(filters),'-map','[vfinal]','-map','8:a:0','-map','9:s:0',
       '-c:v','libx264','-preset','medium','-crf','18','-threads','4',
       '-pix_fmt','yuv420p','-r','30','-frames:v','1800','-c:a','aac','-b:a','192k','-ar','48000',
       '-c:s','mov_text','-metadata:s:s:0','language=spa','-metadata:s:a:0','language=spa',
       '-metadata','title=ENSIU 2026 - Anticipar para Incluir',
       '-metadata','comment=Voz sintetica Microsoft es-CO-GonzaloNeural; evidencia del repositorio Saber Pro.',
       '-t','60','-movflags','+faststart',str(base/'AUDIOVISUAL_ENSIU2026_60s.mp4')]
print('Ensamblando ocho escenas, voz y subtítulos. Salida: AUDIOVISUAL_ENSIU2026_60s.mp4',flush=True)
subprocess.run(args,check=True)
result=json.loads(subprocess.check_output([ffprobe,'-v','error','-show_entries',
    'format=duration,size:stream=index,codec_name,codec_type,width,height,r_frame_rate,duration,nb_frames,sample_rate',
    '-of','json',str(base/'AUDIOVISUAL_ENSIU2026_60s.mp4')],text=True))
video=next(s for s in result['streams'] if s['codec_type']=='video')
audio=next(s for s in result['streams'] if s['codec_type']=='audio')
assert video['nb_frames']=='1800' and video['r_frame_rate']=='30/1'
assert float(result['format']['duration'])==60 and float(video['duration'])==60
assert abs(float(audio['duration'])-60)<0.001
(base/'VERIFICACION_VIDEO.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print('Verificado: 1920 x 1080, 30 fps, 1800 fotogramas, 60.000 segundos.',flush=True)
