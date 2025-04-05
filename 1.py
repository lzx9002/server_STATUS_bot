def format_size(byte_size):
    """将字节数转换为人类可读的格式"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if byte_size < 1024.0:
            return f"{byte_size:.2f} {unit}"
        byte_size /= 1024.0
    return f"{byte_size:.2f} PB"


def format_network(network_data):
    """格式化网络接口信息"""
    output = []
    output.append("=== 网络接口状态 ===")

    # 汇总总流量
    total_up = format_size(network_data["upTotal"])
    total_down = format_size(network_data["downTotal"])
    output.append(f"总上传流量: {total_up} | 总下载流量: {total_down}")
    output.append(f"当前上传速度: {network_data['up']:.2f} MB/s | 当前下载速度: {network_data['down']:.2f} MB/s")
    output.append("-" * 50)

    # 遍历每个网络接口
    for interface, stats in network_data["network"].items():
        if interface == "lo": continue  # 跳过本地回环接口

        up_total = format_size(stats["upTotal"])
        down_total = format_size(stats["downTotal"])
        output.append(f"接口 [{interface}]:")
        output.append(f"  上传总量: {up_total} | 下载总量: {down_total}")
        output.append(f"  当前上传速度: {stats['up']:.2f} MB/s | 当前下载速度: {stats['down']:.2f} MB/s")
        output.append(f"  上传包数量: {stats['upPackets']:,} | 下载包数量: {stats['downPackets']:,}")
        output.append("-" * 50)

    return "\n".join(output)


def format_system(data):
    """格式化系统信息"""
    output = []
    output.append("=== 系统概览 ===")
    output.append(f"|系统名称: {data['title']} "
                  f"| 运行时间: {data['time']}")
    output.append(f"|系统版本: {data['system']} "
                  f"| 宝塔版本: {data['version']}")
    output.append(f"|网站数量: {data['site_total']} "
                  f"| FTP账户: {data['ftp_total']} "
                  f"| 数据库: {data['database_total']}")
    output.append("-" * 50)
    return "\n".join(output)


def format_cpu(data):
    """格式化CPU信息"""
    output = []
    output.append("=== CPU状态 ===")

    # 解析CPU信息（根据原始数据结构适配）
    cpu_info = data["cpu"]
    core_info = cpu_info[2]
    output.append(f"| 处理器型号: {cpu_info[3]}")
    output.append(f"| 逻辑核心数: {cpu_info[4]} "
                  f"| 线程数: {cpu_info[5]}")
    output.append(f"| 当前负载: 用户进程 {data['cpu_times']['user']:.1f} "
                  f"| 系统进程 {data['cpu_times']['system']:.1f}")
    output.append(f"| 空闲率: {data['cpu_times']['idle']:.1f}% "
                  f"| 总进程数: {data['cpu_times']['总进程数']}")
    output.append("-" * 50)
    return "\n".join(output)


def format_memory(data):
    """格式化内存信息"""
    output = []
    output.append("=== 内存状态 ===")

    mem_total = format_size(data["mem"]["memTotal"] * 1024 ** 2)  # 原始数据单位转换
    mem_used = format_size(data["mem"]["memRealUsed"] * 1024 ** 2)
    mem_free = format_size(data["mem"]["memFree"] * 1024 ** 2)

    output.append(f"| 总内存: {mem_total} "
                  f"| 已用内存: {mem_used} "
                  f"| 空闲内存: {mem_free}")
    output.append(f"| 缓存内存: {format_size(data['mem']['memCached'] * 1024 ** 2)}")
    output.append(f"| 可用内存: {format_size(data['mem']['memAvailable'] * 1024 ** 2)}")
    output.append("-" * 50)
    return "\n".join(output)


def format_disk(data):
    """格式化磁盘信息"""
    output = []
    output.append("=== 磁盘状态 ===")

    for disk in data["disk"]:
        total = format_size(disk["byte_size"][0])
        used = format_size(disk["byte_size"][0] - disk["byte_size"][2])
        percent = disk["size"][3]

        output.append(f"| 挂载点: {disk['path']} "
                      f"| 文件系统: {disk['filesystem']}")
        output.append(f"| 总空间: {total} "
                      f"| 已用空间: {used} "
                      f"| 使用率: {percent}")
        output.append(f"| inode使用率: {disk['inodes'][3]}")
        output.append("-" * 50)

    return "\n".join(output)


def main(data):
    """主格式化函数"""
    report = []
    report.append(format_system(data))
    report.append(format_cpu(data))
    report.append(format_memory(data))
    report.append(format_disk(data))
    report.append(format_network(data))

    # 添加负载信息
    report.append("=== 系统负载 ===")
    report.append(
        f"| 1分钟负载: {data['load']['one']:.2f} "
        f"| 5分钟负载: {data['load']['five']:.2f} "
        f"| 15分钟负载: {data['load']['fifteen']:.2f}")
    report.append(f"| 负载阈值: {data['load']['safe']}/{data['load']['max']}")

    return "\n".join(report)


# 使用示例
if __name__ == "__main__":
    # 这里替换为实际的监控数据
    monitoring_data = {...}  # 替换为实际数据

    formatted_report = main(monitoring_data)
    print(formatted_report)