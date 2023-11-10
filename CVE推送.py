import requests
import json
import datetime
import time

def search_github_repositories(query, access_token, created_date, page=1, per_page=30):
    url = f"https://api.github.com/search/repositories?q={query}+created:>{created_date}&page={page}&per_page={per_page}"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)

    print(f"GitHub API URL: {url}")
    print(f"GitHub API Response: {response.text}")

    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        print(f"Error searching GitHub repositories: {response.status_code}")
        return None

def get_latest_commit_url(owner, repo, access_token):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)

    print(f"GitHub API URL for latest commit: {url}")
    print(f"GitHub API Response for latest commit: {response.text}")

    if response.status_code == 200:
        commits = response.json()
        if commits:
            latest_commit_sha = commits[0].get('sha', '')
            return f"https://github.com/{owner}/{repo}/commit/{latest_commit_sha}"
    else:
        print(f"Error getting latest commit URL: {response.status_code}")
        return None

def send_to_dingtalk(url, dingtalk_webhook):
    headers = {"Content-Type": "application/json"}
    payload = {
        "msgtype": "text",
        "text": {
            "content": f"Latest GitHub commit with 'CVE': {url}"
        }
    }

    response = requests.post(dingtalk_webhook, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        print("Sent to DingTalk successfully.")
    else:
        print(f"Error sending to DingTalk: {response.status_code}")

if __name__ == "__main__":
    # 替换为你的 GitHub 访问令牌和 DingTalk Webhook
    # 替换为你的 GitHub 访问令牌和 DingTalk Webhook
    # 替换为你的 GitHub 访问令牌和 DingTalk Webhook
    # 重要的事情说三遍！！！
    # GitHub 访问令牌的权限一定要给满！！
    github_access_token = "your-github-access-token"
    dingtalk_webhook = "https://oapi.dingtalk.com/robot/send?access_token=your-dingtalk-access-token"

    # 计算 30 天前的日期
    thirty_days_ago = datetime.datetime.now() - datetime.timedelta(days=30)
    created_date = thirty_days_ago.strftime("%Y-%m-%dT%H:%M:%SZ")

    # GitHub 查询条件
    github_query = "CVE"

    # 开始搜索 GitHub 仓库并推送最新链接到 DingTalk
    page = 1
    while True:
        github_repositories = search_github_repositories(github_query, github_access_token, created_date, page=page)

        if github_repositories:
            for repo in github_repositories:
                owner = repo.get('owner', {}).get('login', '')
                repo_name = repo.get('name', '')

                # 获取仓库的最新提交链接
                latest_commit_url = get_latest_commit_url(owner, repo_name, github_access_token)

                if latest_commit_url:
                    # 推送到 DingTalk
                    send_to_dingtalk(latest_commit_url, dingtalk_webhook)

            page += 1
            # 休眠 10 秒，避免频繁请求
            # 如果觉得太长可以修改为5s
            time.sleep(10)
        else:
            break
