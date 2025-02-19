# ==== 问题数据提取工具 ====
import pandas as pd
import os
import re

class DataQualityChecker:
    def __init__(self, filepath):
        self.filepath = filepath
        self.report = {
            'date_errors': [],
            'applicant_errors': [],
            'ipc_errors': []
        }
        
    def _safe_read_csv(self):
        """处理不同编码格式"""
        try:
            return pd.read_csv(self.filepath)
        except UnicodeDecodeError:
            return pd.read_csv(self.filepath, encoding='gbk')
    
    def check_dates(self, df):
        """检测日期异常"""
        date_columns = ['申请日期', '优先权日']
        ipc_pattern = re.compile(r'^[A-H]\d{2}[A-Z]?$')  # 标准IPC格式
        
        for idx, row in df.iterrows():
            # IPC格式检测
            ipc = str(row['IPC - 现版']).strip()
            if not ipc_pattern.match(ipc):
                self.report['ipc_errors'].append(row.to_dict())
                
        return df[df.index.isin([x['index'] for x in self.report['ipc_errors']])]

    def generate_report(self, output_dir):
        """生成问题数据样本"""
        os.makedirs(output_dir, exist_ok=True)
        df = self._safe_read_csv()
        
        # 生成各问题CSV
        date_issues = self.check_dates(df)
        if not date_issues.empty:
            date_issues.to_csv(os.path.join(output_dir, "date_issues.csv"), index=False)
            
        applicant_issues = self.check_applicants(df)
        if not applicant_issues.empty:
            applicant_issues.to_csv(os.path.join(output_dir, "applicant_issues.csv"), index=False)
            
        ipc_issues = self.check_ipc(df)
        if not ipc_issues.empty:
            ipc_issues.to_csv(os.path.join(output_dir, "ipc_issues.csv"), index=False)
            
        print(f"问题数据已保存至: {output_dir}")

# ==== 使用说明 ====
if __name__ == "__main__":
    # 配置参数
    DATA_PATH = r"E:\solid-state patent data\csv_cleaned_ipc.csv"
    OUTPUT_DIR = r"E:\solid-state patent data\新建文件夹\debug_samples"
    
    checker = DataQualityChecker(DATA_PATH)
    checker.generate_report(OUTPUT_DIR)
