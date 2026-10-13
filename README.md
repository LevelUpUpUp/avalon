# Avalon 隐私与支持网站

独立于应用源码的中英文静态隐私政策和支持页面。无第三方依赖、统计脚本、Cookie、外部字体或远程嵌入。托管服务仍可能处理 IP 和访问日志，政策正文已说明。

## 修改内容

- `content/privacy.zh-CN.md`、`content/privacy.en.md`：中英文隐私政策。
- `content/support.zh-CN.md`、`content/support.en.md`：中英文支持页面。
- `site.json`：真实开发者姓名／主体、公开联系邮箱、更新日期。不要将登录邮箱默认当成公开邮箱。
- `assets/style.css`：页面样式。

名称建议对应 App Store 的真实开发者／提供者，组织可同时标注品牌。保持两种语言的实质内容一致。当前条款以 Avalon 仓库 2026-10-13 的发布功能和隐私文档为依据；政策不是“终身不变”的承诺。当前发布包不含人脸识别，默认局域网 HTTP 无传输加密，不提供开发者托管云图库。新功能、在线服务、支付或数据处理方式改变时，应更新政策并核对商店隐私声明。

## 本地预览

Python 3.9 或更新版本即可，无需安装依赖。

```sh
python3 scripts/build.py --allow-draft
python3 scripts/check.py --allow-draft
python3 -m http.server 8080 --bind 127.0.0.1 --directory _site
```

打开 `http://127.0.0.1:8080/`。未填写主体和邮箱时显示草稿提示。`--allow-draft` 仅用于本地预览。

## 发布到 GitHub Pages

1. 在 `site.json` 中填写真实名称和可接收邮件的邮箱，并确认更新日期。
2. 运行 `python3 scripts/build.py` 和 `python3 scripts/check.py`。缺少名称或有效邮箱时正式构建失败；不会用占位政策继续部署。
3. 提交并推送到 `main`。仓库 Settings → Pages → Build and deployment → Source 选择 **GitHub Actions**。使用免费 GitHub 账号时，仓库需要公开。
4. 工作流成功后，以 GitHub Pages 返回的网址为准。当前远程为 `https://github.com/LevelUpUpUp/avalon.git`，默认地址预计为 `https://levelupupup.github.io/avalon/`；当前尚未部署，也未验证该地址。
5. 用无痕窗口及实际目标用户网络检查：无需登录、无需 VPN，能打开中英文页面、联系邮箱及链接。

发布时 `_site/` 是唯一上传内容，应用源码不需要放进此仓库。`_site/` 是生成目录，已忽略。所有页面使用相对链接，兼容项目路径 `/avalon/`。

## 上架时的链接

如果默认 Pages 地址生效，可使用：

- 隐私政策（中文）：`https://levelupupup.github.io/avalon/privacy/`
- 隐私政策（英文）：`https://levelupupup.github.io/avalon/privacy/en/`
- 支持（中文）：`https://levelupupup.github.io/avalon/support/`
- 支持（英文）：`https://levelupupup.github.io/avalon/support/en/`

在 App Store Connect 对应语言资料中填写实际可访问的网址。应用打包时的 `PRIVACY_POLICY_URL`、`SUPPORT_URL` 也应配置为正式网址（Avalon 当前代码使用一组构建参数，网页内可切换语言）。隐私网页不替代隐私清单或 App Privacy 数据声明；应结合最终签名包核实。

现有构建脚本使用方式示例（在应用源码的 `avalon-install` 目录）：

```sh
PRIVACY_POLICY_URL=https://levelupupup.github.io/avalon/privacy/ SUPPORT_URL=https://levelupupup.github.io/avalon/support/ ./build_package.sh
```

这里只准备本地文件和发布工作流，不自动推送、修改仓库公开权限或启用 Pages。

参考：[Apple 隐私要求](https://developer.apple.com/app-store/review/guidelines/#privacy)、[GitHub Pages 发布流程](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)、[GitHub 隐私声明](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement)。
