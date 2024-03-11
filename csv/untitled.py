commit_type = []
commit_info = {}
commit_data = []
file_data = []
commit_id = None
file_sn = 0

commit_cls = ['feat', 'fix', 'docs', 'test', 'refact', 'style', 'chore']
# 텍스트 파일을 한 줄씩 읽어옵니다.
with open("./txt/gitLog_240124.txt", "r", encoding="utf-8") as file:
    commit_dtl = ""  # 여러 줄의 commit_dtl을 저장할 변수 추가
    # 각 라인을 처리
    for i, line in enumerate(file):    
        line = line.strip()
        #commit 정보 처리
        if line.startswith("commit_") or line.startswith("Author"):
            parts = line.split('||')
            column_name = parts[0].strip() # 컬럼명
            value = parts[1].strip()       # 컬럼값
        
            commit_info[column_name] = value
            # 현재 commit_id 설정
            if column_name == 'commit_id':
                commit_id = value
            # commit_dtl 처리
            if column_name == 'commit_dtl': 
                commit_dtl += value + " "  # 여러 줄을 공백을 포함하여 하나의 문자열로 저장
        # commit 관련 파일 처리    
        elif line and line[0].isupper() and not line.startswith("R100"):
            parts = line.split()
            if len(parts) > 1:
                file_sn = file_sn + 1
                # file_df에 새로운 행 추가
                file_data.append({'commit_id': commit_id + '', 'file_sn': file_sn, 'job_cls': parts[0], 'file_path': parts[1]})
    
    # commit_info에 저장된 commit_dtl을 업데이트
    commit_info['commit_dtl'] = commit_dtl.strip()
    # commit_data에 commit_info 추가
    commit_data.append(commit_info)

# 데이터를 데이터프레임으로 변환합니다.
commit_df = pd.DataFrame(commit_data)
file_df = pd.DataFrame(file_data)
