# 维护者发布步骤

本仓库只发布用户文档、示例、Homebrew Formula 和编译好的安装包。构建使用的源码仓库与本仓库分别提交；开始升级前先提交已有改动，记录用于本次发布的源码提交和文档提交。

1. 确定版本和产物清单。Windows 完整 ZIP、安装程序，macOS Apple 芯片完整 ZIP、仅 CLI 的 tar.gz，Linux amd64 DEB 应来自同一个源码提交。不要把构建目录、源码归档、内部路径或凭据作为 Release 附件。
2. 完成该提交的 Rust 测试；有窗口的包完成 Flutter 分析、测试、平台构建和窗口启动检查。解开最终安装包，使用包内程序跑 `--version`、`--help`，按 `skill/SKILL.md` 的快速自测在临时目录验证。记录实际结果，不沿用旧版测试数字。
3. 同步本仓库中英文 README、`skill/INSTALL.md`、通用 SKILL 内容和命令 / 格式参考。保留公开 MP157 教程、`skill/examples/lib`、`skill/build/st/board.PcbDoc` 及它们的相对路径。检查命令参考确实由本次程序生成。
4. 组装完整包时使用公开文档和示例；检查压缩包内没有源码仓库说明、内部地址或本机路径。macOS CLI tar.gz 的根目录必须直接包含 `easyedatool`，与 Formula 的安装逻辑一致。
5. 为最终附件计算 SHA256，验证 ZIP、tar.gz、DEB 可解包，核对包内版本。将 macOS CLI tar.gz 的实际 SHA256 写入 `Formula/easyedatool.rb`，同时更新 URL、版本和 Formula 的版本测试。禁止填写占位校验值。
6. 在 `CHANGELOG.md` 填上本次完成的验证结果及限制。核对 README 的平台、文件名与实际附件一致；缺少或未测的平台明确注明。文档提交后创建 GitHub Release 并上传对应附件，发布后重新下载核验版本和 SHA256。
7. APT 和 winget 是独立渠道。APT 更新并检查候选版本；winget 只有官方源确实收录且能查询到目标版本后，才在文档中列为可用。Homebrew Formula 应能下载相应附件且校验通过。单一平台发布完成不代表全部渠道同步完成。

公开仓库及 Release 的目标始终是 [cc38324/PcbCliTool](https://github.com/cc38324/PcbCliTool)。发布说明中不加入内部源码远端、机器地址、登录用户名或构建凭据。
