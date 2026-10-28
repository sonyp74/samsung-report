name: Daily Samsung Report Update

on:
  schedule:
    - cron: '30 23 * * *'
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    
    # 👇 이 권한 설정을 추가해주면 403 권한 에러가 해결됩니다!
    permissions:
      contents: write

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.x'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install beautifulsoup4

    - name: Run Crawler
      run: python crawler.py

    - name: Commit and Push Changes
      run: |
        git config --global user.name "github-actions[bot]"
        git config --global user.email "github-actions[bot]@users.noreply.github.com"
        git add index.html
        git diff --quiet && git diff --staged --quiet || (git commit -m "Auto Update Samsung Report" && git push)
