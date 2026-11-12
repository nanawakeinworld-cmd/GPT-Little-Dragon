# 安装指南 · Installation

> **English quick steps:** install MaCursor (macOS 13+) → double-click
> `Cursor/GPT-Little-Dragon-v16.cursor` → select the theme → **Apply** → install
> the Helper Tool → reset the system pointer colour. Details below.

## 0. 先确认

| 项目 | 要求 |
|---|---|
| 系统 | macOS 13 Ventura 或更高 |
| 芯片 | Apple Silicon 或 Intel 均可 |
| 必需软件 | [MaCursor](https://github.com/writronic/MaCursor/releases/latest) |
| 主题文件 | `Cursor/GPT-Little-Dragon-v16.cursor`（约 1.7 MB） |

> 这是 MaCursor 专用的 `.cursor` 主题包，macOS 不能直接双击安装。
> 请先装 MaCursor。

## 1. 安装 MaCursor

1. 打开 [MaCursor Releases](https://github.com/writronic/MaCursor/releases/latest)。
2. 下载最新 `.dmg`。
3. 打开 dmg，把 **MaCursor** 拖进 `/Applications`。
4. 首次启动时按欢迎窗口的提示完成设置。

也可以用 Homebrew：

```bash
brew install --cask writronic/tap/macursor
```

MaCursor 的发行版由 Apple 签名并公证，正常情况不会触发“无法验证开发者”。

## 2. 导入主题

任选一种：

- **双击** `Cursor/GPT-Little-Dragon-v16.cursor`；
- 把文件**拖进** MaCursor 主窗口；
- MaCursor 菜单 `File → Import Theme…`，选择该文件。

导入后，左侧列表会出现 **「GPT 小龙 v16」**。

## 3. 应用主题

1. 在左侧选中「GPT 小龙 v16」。
2. 点 **Apply**。
3. 把鼠标移到桌面或 Finder 窗口上，确认指针已经变化。

## 4. 安装 Helper Tool（强烈建议）

不装的话，重启、休眠唤醒或切换用户后，指针可能恢复成系统默认。

1. 打开 `MaCursor → Settings → General`。
2. 在 **Helper Tool** 一栏点 **Install**。
3. 按提示授权。

Helper 是一个轻量登录项，会在登录时自动重新应用主题。

## 5. 重置系统指针颜色

这一步很容易漏，但很关键：

1. 打开 `系统设置 → 辅助功能 → 显示`。
2. 找到 **指针颜色**。
3. 点 **重置颜色**，恢复成默认的黑白指针。

如果系统指针被改成了彩色，自定义主题可能只在部分窗口生效。

## 6. 验证清单

- [ ] 桌面上的普通指针变成紫色三角箭头。
- [ ] 移到文本输入框上，出现笔记本电脑 + I-beam。
- [ ] 拖拽窗口或文件时，出现对应的角色指针。
- [ ] 等待动画（转圈/忙碌）能播放。
- [ ] 重启后指针仍然是主题样式。
- [ ] 深色 / 浅色模式下边缘都清晰。

## 7. 已知限制

以下应用会自绘光标，主题无法覆盖：

- 终端（Terminal / iTerm2 的文本光标）
- Adobe 系列
- 大多数游戏
- 部分 Electron 应用

这是 macOS 的机制限制，不是主题安装失败。

## 8. 出问题了？

见 [`Troubleshooting.md`](Troubleshooting.md)，或回到 MaCursor 执行
`File → Reset System Cursor` 恢复默认指针。
