from pathlib import Path
import pandas as pd,numpy as np,joblib,json,warnings,hashlib
warnings.filterwarnings('ignore')
o=Path('outputs/CONACIC2026'); d=pd.read_csv('data/processed/saber_pro_features.csv',low_memory=False); train=d[d['AÑO']<2024];test=d[d['AÑO']==2024];res={'rows':len(d),'years':d.groupby('AÑO').size().to_dict(),'columns':len(d.columns),'train_monotonic_year':bool(train['AÑO'].is_monotonic_increasing),'models':{}}
for n in ['ridge','lasso','lgbm']:
 try:
  f=Path(f'outputs/{n}_model.pkl');p=joblib.load(f);pred=p.predict(test);y=test.PROMEDIO_GLOBAL.to_numpy();e=y-pred
  info={'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'RMSE':float(np.sqrt(np.mean(e**2))),'MAE':float(np.mean(abs(e))),'R2':float(1-np.sum(e**2)/np.sum((y-y.mean())**2)),'features':list(p.feature_names_in_),'pipeline':str(p)}
  encoder=p.named_steps['preprocessor'].named_transformers_['cat'].named_steps['encoder']
  info['target_encoder_mode']=encoder.target_type_;info['target_encoder_class_count']=len(encoder.classes_) if encoder.classes_ is not None else 0;info['transformed_column_count']=len(p.named_steps['preprocessor'].get_feature_names_out())
  if n=='lgbm':
   info['params']=p.named_steps['model'].get_params();info['transformed_features']=list(p.named_steps['preprocessor'].get_feature_names_out());
  res['models'][n]=info
 except Exception as ex:res['models'][n]={'error':str(ex)}
# Internal splits reproduce indices, not training
from sklearn.model_selection import TimeSeriesSplit
res['fold_years']=[{'train':sorted(train.iloc[a]['AÑO'].unique().tolist()),'val':sorted(train.iloc[b]['AÑO'].unique().tolist())} for a,b in TimeSeriesSplit(n_splits=4).split(train)]
res['optuna80_years']={'train':sorted(train.iloc[:int(len(train)*.8)]['AÑO'].unique().tolist()),'val':sorted(train.iloc[int(len(train)*.8):]['AÑO'].unique().tolist())}
k=['ID_INSTITUCION','ID_PROGRAMA_ACAD','NOMBRE_PRUEBA'];s=d.sort_values(k+['AÑO']); prev=s.groupby(k)['AÑO'].shift(1);res['lag1_gaps_gt1']=int(((s['AÑO']-prev)>1).sum());res['lag_check_max_error']=float((s.groupby(k)['PROMEDIO_GLOBAL'].shift(1)-s['lag_1_promedio_global']).abs().max())
(o/'VERIFICACION_DATOS_MODELOS.json').write_text(json.dumps(res,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
print(json.dumps({**res,'models':{k:{a:b for a,b in v.items() if a not in ['pipeline','features','transformed_features','params']} for k,v in res['models'].items()}},indent=2,ensure_ascii=False))
