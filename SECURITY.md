# Security Policy

这个仓库是 Public 仓库。任何本机密钥、会话历史、日志、数据库和用户记忆都不应该提交。

## 提交前检查

运行：

```powershell
pwsh ./scripts/check-secrets.ps1
```

如果检查发现敏感文件，删除该文件并重新检查。不要用 `git add -f` 绕过 `.gitignore`。

## 已误提交密钥怎么办

1. 立即撤销或轮换对应 token。
2. 从 Git 历史里清理该文件或该值。
3. 重新运行 `scripts/check-secrets.ps1`。
4. 再推送干净历史。

删除工作区文件不等于删除 Git 历史。密钥只要进过 Public 仓库，就按泄露处理。
