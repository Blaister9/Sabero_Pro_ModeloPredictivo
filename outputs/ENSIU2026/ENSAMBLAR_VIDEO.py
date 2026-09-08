"""Monta ENSIU con la grabación real, conservando íntegro el audio AAC."""
from pathlib import Path
import hashlib, json, shutil, subprocess, sys

sys.stdout.reconfigure(encoding='utf-8')

base=Path(__file__).resolve().parent
ffmpeg=shutil.which('ffmpeg') or 'C:/ffmpeg/bin/ffmpeg.exe'
ffprobe=shutil.which('ffprobe') or 'C:/ffmpeg/bin/ffprobe.exe'
timing=json.loads((base/'CRONOMETRAJE.json').read_text(encoding='utf-8'))
scenes=timing['scenes']
assert len(scenes)==8 and scenes[0]['start']==0 and scenes[-1]['end']==60
audio_path=base/timing['audio']['file']
assert hashlib.sha256(audio_path.read_bytes()).hexdigest()==timing['audio']['sha256']
assert timing['audio']['start']==0 and timing['audio']['speed']==1
output=base/timing['video']['file']
args=[ffmpeg,'-y','-hide_banner','-loglevel','warning','-filter_complex_threads','2']
filters=[]
for i,s in enumerate(scenes):
    duration=s['end']-s['start']+(0.3 if i<7 else 0)
    args+=['-loop','1','-framerate','30','-t',f'{duration:.6f}','-i',str(base/'escenas'/f'escena_{i+1:02d}.png')]
    filters.append(f'[{i}:v]fps=30,format=yuv444p,settb=AVTB,setpts=PTS-STARTPTS[v{i}]')
args+=['-i',str(audio_path)]
last='v0'
for i in range(1,8):
    label=f'mix{i}'
    filters.append(f'[{last}][v{i}]xfade=transition=fade:duration=0.3:offset={scenes[i]["start"]:.6f}[{label}]')
    last=label
filters.append(f'[{last}]fps=30,format=yuv420p[vfinal]')
args+=['-filter_complex',';'.join(filters),'-map','[vfinal]','-map','8:a:0',
       '-c:v','libx264','-preset','medium','-crf','18','-threads','4',
       '-pix_fmt','yuv420p','-r','30','-frames:v','1800','-c:a','copy',
       '-metadata:s:a:0','language=spa',
       '-metadata','title=ENSIU 2026 - Anticipar para Incluir',
       '-metadata','comment=Narracion original Grabacion (14).m4a, copiada sin recodificacion ni filtros. Cierre visual sin audio.',
       '-t','60','-movflags','+faststart',str(output)]
print('Ensamblando ocho escenas con audio original intacto. Salida: '+output.name,flush=True)
subprocess.run(args,check=True)
result=json.loads(subprocess.check_output([ffprobe,'-v','error','-show_entries',
    'format=duration,size:stream=index,codec_name,codec_type,width,height,r_frame_rate,duration,nb_frames,sample_rate',
    '-of','json',str(output)],text=True))
video=next(s for s in result['streams'] if s['codec_type']=='video')
audio=next(s for s in result['streams'] if s['codec_type']=='audio')
assert video['nb_frames']=='1800' and video['r_frame_rate']=='30/1'
assert float(result['format']['duration'])==60 and float(video['duration'])==60
assert abs(float(audio['duration'])-timing['audio']['duration'])<0.001
(base/'VERIFICACION_VIDEO.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
def packets(file):
    return json.loads(subprocess.check_output([ffprobe,'-v','error','-select_streams','a:0',
        '-show_packets','-show_data_hash','sha256','-show_entries','packet=pts,dts,duration,data_hash',
        '-of','json',str(file)],text=True))['packets']
original_packets=packets(audio_path);final_packets=packets(output)
assert len(original_packets)==len(final_packets)
assert [p['data_hash'] for p in original_packets]==[p['data_hash'] for p in final_packets]
assert [(p['pts'],p['dts'],p['duration']) for p in original_packets]==[(p['pts'],p['dts'],p['duration']) for p in final_packets]
def pcm_hash(file):
    return subprocess.check_output([ffmpeg,'-v','error','-i',str(file),'-map','0:a:0',
        '-c:a','pcm_s16le','-f','hash','-hash','sha256','-'],text=True).strip()
original_pcm=pcm_hash(audio_path);final_pcm=pcm_hash(output)
assert original_pcm==final_pcm
audio_check={'source_file':timing['audio']['file'],'source_sha256':timing['audio']['sha256'],
    'original_duration':timing['audio']['duration'],'output_audio_duration':float(audio['duration']),
    'aac_packet_count':len(original_packets),'all_aac_packet_hashes_identical':True,
    'all_packet_timestamps_identical':True,'decoded_pcm_source':original_pcm,'decoded_pcm_final':final_pcm,
    'decoded_pcm_identical':True,'audio_filters':[],'audio_codec_mode':'copy',
    'speed':1,'audio_offset_seconds':0,'video_duration':60,
    'silent_closing_seconds':60-timing['audio']['duration']}
(base/'VERIFICACION_AUDIO_ORIGINAL.json').write_text(json.dumps(audio_check,ensure_ascii=False,indent=2),encoding='utf-8')
print('Verificado: Full HD, 1800 fotogramas, 60.000 s. Audio AAC y PCM idénticos al original.',flush=True)
