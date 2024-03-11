import pandas as pd
import re
# # commit_df 초기화
# commit_df = pd.DataFrame(columns=['commit_id', 'commiter', 'commit_date', 'commit_summ', 'commit_dtl'])
# file_df = pd.DataFrame(columns=['commit_id', 'file_sn', 'job_cls', 'file_path'])

commit_info = {}
commit_data = []
file_data = []
commit_id = None
file_sn = 0
# 텍스트 파일을 한 줄씩 읽어옵니다.
with open("D:/jinee/Git_menuToFile/txt/gitLog_231128.txt", "r", encoding="utf-8") as file:
    # 각 라인을 처리
    for i, line in enumerate(file):    
        line = line.strip()
        #commit 정보 처리
        if line.startswith("commit_") or line.startswith("Author") :
            parts = line.split('||')
            column_name = parts[0].strip() # 컬럼명
            value = parts[1].strip()       # 컬럼값
        
            commit_info[column_name] = value
            # 현재 commit_id 설정
            if column_name == 'commit_id':
                
                commit_id = value
            
            if column_name == 'commit_dtl': 
                # commit_dtl 을 만나면 commit_df에 새로운 행 추가하고 초기화
                commit_data.append(commit_info)
                commit_info = {}
                file_sn = 0
        # commit 관련 파일 처리    
        elif line and line[0].isupper() and not line.startswith("R100"):
            parts = line.split()
            if len(parts) > 1:
                file_sn = file_sn + 1
                # file_df에 새로운 행 추가
                file_data.append({'commit_id': commit_id, 'file_sn': file_sn, 'job_cls': parts[0], 'file_path': parts[1]})
        
# 데이터를 데이터프레임으로 변환합니다.
commit_df = pd.DataFrame(commit_data)
file_df = pd.DataFrame(file_data)

# NaN 값 대체
commit_df.fillna('')
file_df.fillna('')

# 데이터프레임 csv 로 저장
commit_df.to_csv('D:/jinee/Git_menuToFile/csv/commit_info.csv', encoding="utf-8", index=False)
file_df.to_csv('D:/jinee/Git_menuToFile/csv/commit_file_info.csv', encoding="utf-8", index=False)

# commit_df[pd.isnull( commit_df['commit_id'])]
# controller_do.dropna(subset=['controller_file'], inplace=True)