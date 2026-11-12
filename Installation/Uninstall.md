# 卸载与恢复 · Uninstall

> **English quick steps:** MaCursor → `File → Reset System Cursor` → delete the
> theme → quit and remove `/Applications/MaCursor.app` → remove the login item
> and `~/Library/Application Support/MaCursor`.

## 只恢复默认指针（保留 MaCursor）

1. 打开 MaCursor。
2. 菜单 `File → Reset System Cursor`。
3. 指针立即恢复系统默认。

如果指针没有立刻变化，注销后重新登录，或重启。

## 只删除这个主题（保留 MaCursor）

1. 打开 MaCursor。
2. 在左侧列表找到「GPT 小龙 v16」。
3. 右键 → **Delete**（或选中后按 Delete）。
4. 确认删除。

主题文件本身不会被自动删除；如果不再需要，可以把
`Cursor/GPT-Little-Dragon-v16.cursor` 一起删掉。

## 彻底卸载 MaCursor

1. 先执行 `File → Reset System Cursor`。
2. 退出 MaCursor（菜单栏图标 → Quit）。
3. 删除应用：
   ```bash
   rm -rf /Applications/MaCursor.app
   ```
4. 删除支持文件：
   ```bash
   rm -rf ~/Library/Application\ Support/MaCursor
   ```
5. 移除登录项：`系统设置 → 通用 → 登录项`，找到 MaCursor / MaCursorHelper，
   点 `−` 移除。
6. 如果还残留偏好设置，可检查：
   ```bash
   ls ~/Library/Preferences | grep -i macursor
   ```
   确认后再删除对应文件。

> 删除前请确认路径。上面的命令只会动 MaCursor 自己的目录，不会碰系统指针文件。

## 卸载后验证

- [ ] 指针恢复成 macOS 默认样式。
- [ ] 重启后不再出现自定义指针。
- [ ] 登录项列表里没有 MaCursor。
- [ ] `/Applications/MaCursor.app` 已不存在。

## 如果卸载后指针仍然异常

1. 重启 Mac。
2. 打开 `系统设置 → 辅助功能 → 显示 → 指针颜色 → 重置颜色`。
3. 如果仍然异常，参考 [`Troubleshooting.md`](Troubleshooting.md)。
