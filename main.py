from smtpd import program

import pandas as pd
enrollee = pd.read_csv('enrollee.csv')
program = pd.read_csv('program.csv')
program_enrollee = pd.read_csv('program_enrollee.csv')
program_subject = pd.read_csv('program_subject.csv')
subject = pd.read_csv('subject.csv')
enrollee_subject = pd.read_csv('enrollee_subject.csv')
enrollee_achievement = pd.read_csv('enrollee_achievement.csv')
achievement = pd.read_csv('achievement.csv')
department = pd.read_csv('department.csv')

merge1 = pd.merge(enrollee, program_enrollee, on="enrollee_id")
merge1 = pd.merge(merge1, program, on="program_id")

itog1 = merge1.loc[merge1['name_program']. isin(['Мехатроника и робототехника'])]
itog1 = itog1.sort_values(by='name_enrollee', ascending=True)['name_enrollee']
#print(itog1, '\n')
#itog1.to_csv('itog1_results.csv', index=False)

merge2 = pd.merge(subject, program_subject, on='subject_id')
merge2 = pd.merge(merge2, program, on='program_id')
itog2 = merge2[merge2.name_subject=='Информатика']['name_program']
#print(itog2, '\n')
#itog2.to_csv('itog2_results.csv', index=False)

merge3 = pd.merge(enrollee_subject, subject, on='subject_id')
itog3 = merge3.groupby('name_subject')['result'].agg(['min', 'max', 'mean', 'count'] )
itog3.columns = ['Минимум', 'Максимум', 'Среднее', 'Количество']
itog3 = itog3.reset_index()
#print(itog3)
#itog3.to_csv('itog3_results.csv', index=False)

itog4 = program_subject.groupby('program_id')['min_result'].min().reset_index()
itog4 = itog4[itog4['min_result']>=40]
itog4 = pd.merge(itog4, program, on='program_id', how='left')
itog4 = itog4[['name_program']].sort_values('name_program')
#print(itog4['name_program'])
#itog4.to_csv('itog4_results.csv', index=False)

itog5 = program[program['plan'] == max(program['plan'])].loc[:, ['name_program', 'plan']]
#print(itog5)
#itog5.to_csv('itog5_results.csv', index=False)

itog6 = pd.merge(pd.merge(enrollee, enrollee_achievement, on='enrollee_id', how='left'), achievement, on='achievement_id', how='left')
itog6 = itog6.groupby('name_enrollee')['bonus'].agg(['sum']).sort_values('name_enrollee')
itog6.columns = ['Бонус']
itog6 = itog6.reset_index()
#print(itog6)
#itog6.to_csv('itog6_results.csv', index=False)

itog7 = pd.merge(program_enrollee, program, on='program_id', how='left')
itog7 = itog7.groupby(['name_program', 'plan', 'department_id'])['enrollee_id'].agg(['count'])
itog7.columns = ['Количество']
itog7 = pd.merge(itog7.reset_index(), department, on='department_id', how='left')
itog7 = itog7[['name_department', 'name_program', 'plan', 'Количество']]
itog7['Конкурс'] = round(itog7['Количество']/itog7['plan'], 2)
itog7 = itog7.sort_values('Конкурс', ascending=False)
#print(itog7)
#itog7.to_csv('itog7_results.csv', index=False)

inf = program_subject[program_subject['subject_id'].isin(subject[subject['name_subject'].isin(['Информатика'])]['subject_id'])]
mat = program_subject[program_subject['subject_id'].isin(subject[subject['name_subject'].isin(['Математика'])]['subject_id'])]
itog8 = pd.merge(pd.merge(inf, mat, on='program_id'), program, on='program_id',how='left')['name_program']
#print(itog8)
#itog8.to_csv('itog8_results.csv', index=False)

itog9 = pd.merge(pd.merge(program_subject, program_enrollee, on='program_id'), enrollee_subject, on=['enrollee_id', 'subject_id'])
itog9 = itog9.groupby(['enrollee_id', 'program_id'])['result'].agg(['sum'])
itog9.columns = ['itog']
itog9 = itog9.reset_index()
itog9 = pd.merge(pd.merge(itog9, program, on='program_id', how='left'), enrollee, on='enrollee_id', how='left')[['name_program', 'name_enrollee', 'itog']]
itog9 = itog9.sort_values(['name_program', 'itog'], ascending=[True, False])
print(itog9)
itog9.to_csv('itog9_results.csv', index=False)

