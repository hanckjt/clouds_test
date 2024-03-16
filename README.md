# 云服务节点Ping速度测试器

云服务节点Ping速度测试器是一个基于Python的工具，旨在测试和比较全球知名的几家云服务器厂商的全球各节点的ping速度。该工具允许您测量不同云服务器在全球的网络延迟，为每个云提供商的网络性能和可靠性提供见解。

## 功能特点

- **并发测试**：支持并发执行，可同时测试多个云提供商节点。
- **灵活的目标选择**：允许指定要测试的云提供商和位置，提供定制化测试场景。
- **性能优选显示**：显示速度最优的服务器，并用颜色标记，易于识别最佳性能服务器。

## 开始使用

### 准备工作

在运行云服务节点Ping速度测试器之前，请确保您的系统上已安装Python。本项目已在Python 3.6及以上版本测试通过。

### 安装

1. **克隆仓库：**

   ```bash
   git clone https://github.com/hanckjt/clouds_test.git
   cd clouds_test
   ```
2. **设置虚拟环境并安装依赖：**

   - 在Windows上，运行或直接双击 `clouds_test.cmd`会自动创建虚拟环境，安装依赖，并运行程序。
   - 在Linux或macOS上，使用 `clouds_test.sh`达到同样的目的，但因为Linux的[ICMP权限的限制]()，如果不是root用户会提示sudo的权限。
   - 也可以手动安装 `pip install -r requirements.txt`，然后运行 `clouds_test.py`。

### 使用方法

运行 `clouds_test.py`（或直接使用两个自动脚本是一样的），并添加可选参数以开始测试ping速度。可用选项包括：

- `-f`, `--file`：指定包含云服务器信息的CSV文件路径。默认为 `cloud_servers.csv`。
- `-c`, `--cloud`：指定要测试的云提供商。可以包括多个提供商。
- `-l`, `--location`：指定要测试的位置。可以包括多个位置。
- `-t`, `--top`：指定基于速度显示的最佳性能服务器数量。默认为5。

**示例命令：**

```bash
clouds_test.cmd
```

如果没有任何参数，就会测试csv文件里所有的服务器
![image](https://github.com/hanckjt/clouds_test/assets/16874002/9107236a-60db-43a0-a0e2-407954767b96)


---

```bash
./clouds_test.sh -l China
```

这会显示所有云服务器厂商在国内服务器的延迟

---

```bash
python clouds_test.py --cloud Aliyun Tencent Huawei Ucloud --location "Hong Kong" Japan --top 6
```

此命令测试国内阿里云、腾讯云、华为云和Ucloud服务器在香港与日本地区的延迟，并显示前6名性能优异的服务器。

## 贡献

欢迎贡献！请随时提交拉取请求、报告错误和建议功能。

## 许可证

本项目根据MIT许可证授权 - 详见[LICENSE.md](LICENSE)文件。
