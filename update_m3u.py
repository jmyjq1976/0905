import requests
import os
import sys

def update_m3u():
    url = os.environ.get("M3U_URL", "https://iptv.yang-1989.xyz/playlist.m3u")
    output_file = "playlist.m3u"  # 仓库中保存的文件名
    
    try:
        print(f"开始从 {url} 下载最新 M3U 文件...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        new_content = response.text
        
        # 检查文件是否已存在且内容相同，避免无意义的提交
        if os.path.exists(output_file):
            with open(output_file, 'r', encoding='utf-8') as f:
                if f.read() == new_content:
                    print("文件内容无变化，无需更新。")
                    return False
        
        # 写入新内容
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print("M3U 文件更新成功！")
        return True
        
    except Exception as e:
        print(f"下载或更新失败: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    updated = update_m3u()
    # 将结果写入环境变量文件，供后续 Action 步骤读取
    with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
        f.write(f"updated={str(updated).lower()}\n")
