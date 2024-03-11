#!/usr/bin/env python
# coding: utf-8

# ## 1. 커밋로그 추출해서 커밋 정보과 커밋 파일 목록으로 나눠서 csv 파일로 저장

# In[1]:
import pandas as pd
import re
# # commit_df 초기화
# commit_df = pd.DataFrame(columns=['commit_id', 'commiter', 'commit_date', 'commit_summ', 'commit_dtl'])
# file_df = pd.DataFrame(columns=['commit_id', 'file_sn', 'job_cls', 'file_path'])
commit_type = []
commit_info = {}
commit_data = []
file_data = []
commit_id = None
file_sn = 0

commit_cls = ['feat', 'fix', 'docs', 'test', 'refact', 'style', 'chore']
# 텍스트 파일을 한 줄씩 읽어옵니다.
with open("./txt/gitLog_240221_2.txt", "r", encoding="utf-8") as file:
    commit_dtl = ""  # 여러 줄의 commit_dtl을 저장할 변수 추가
    # 각 라인을 처리
    for i, line in enumerate(file):    
        line = line.strip()
        #commit 정보 처리
        if line.startswith("commit_") or line.startswith("Author"):
            parts = line.split("||")
            column_name = parts[0].strip() # 컬럼명
            value = parts[1].strip()       # 컬럼값
        
            commit_info[column_name] = value
            # 현재 commit_id 설정
            if column_name == "commit_id":
                commit_id = value
            elif column_name == "commit_dtl": 
                commit_dtl = value + " "
        elif line.startswith("file_list"): 
            # commit_info에 저장된 commit_dtl을 업데이트
            commit_info['commit_dtl'] = commit_dtl.strip()
            commit_dtl = ""
            # file_list 을 만나면 commit_df에 새로운 행 추가하고 초기화
            commit_data.append(commit_info)
            commit_info = {}
            file_sn = 0
        elif commit_dtl != "": 
            commit_dtl += line + " "  # 여러 줄을 공백을 포함하여 하나의 문자열로 저장            
        # commit 관련 파일 처리    
        elif line and line[0].isupper():
            parts = line.split()
            if len(parts) > 1:
                file_sn = file_sn + 1
                # file_df에 새로운 행 추가
                file_data.append({'commit_id': commit_id + '', 'file_sn': file_sn, 'job_cls': parts[0], 'file_path': parts[1]})
    
# 데이터를 데이터프레임으로 변환합니다.
commit_df = pd.DataFrame(commit_data)
file_df = pd.DataFrame(file_data)

# 날짜 컬럼 추출
commit_df['commit_dt'] = pd.to_datetime(commit_df['commit_dt'])

# 커밋 유형 추출하기
keywords = ['feat', 'fix', 'docs', 'test', 'refact', 'style', 'chore']
# Extract the first part and remove leading/trailing whitespaces
commit_df['first_part'] = commit_df['commit_msg'].str.split(':').str[0].str.strip()

# Check if 'first_part' contains any keyword
commit_df['contains_keyword'] = commit_df['first_part'].isin(keywords)

# Filter DataFrame based on the condition
filtered_df = commit_df[commit_df['contains_keyword']]

# Assign values to 'commit_cls' column for the filtered rows
commit_df.loc[commit_df['contains_keyword'], 'commit_cls'] = filtered_df['commit_msg'].str.split(':').str[0]
commit_df.loc[commit_df['contains_keyword'], 'commit_msg'] = filtered_df['commit_msg'].str.split(':').str[1]

commit_df = commit_df.drop(['contains_keyword', 'first_part'], axis=1)

# NaN 값 대체
commit_df.fillna('')
file_df.fillna('')

# 데이터프레임 csv 로 저장
commit_df.to_csv('./csv/commit_info.csv', encoding="utf-8", index=False)
file_df.to_csv('./csv/commit_file_info.csv', encoding="utf-8", index=False)

# commit_df[pd.isnull( commit_df['commit_id'])]
# controller_do.dropna(subset=['controller_file'], inplace=True)
# commit_df[pd.isnull( commit_df['commit_id'])]

# commit_df.dropna(subset=['commit_id'], inplace=True)
# 결과 출력
commit_df.info()

# commit_df = pd.read_csv('./csv/commit_info.csv', encoding="utf-8")
# file_df = pd.read_csv('./csv/commit_file_info.csv', encoding="utf-8")

