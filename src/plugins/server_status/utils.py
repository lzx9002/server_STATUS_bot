# -*- coding: utf-8 -*-
# @Project : server_STATUS_bot
# @File    : utils.py
# @IDE     : PyCharm
# @Author  : lzx9002
# @Time    : 2025/4/5 14:46
import hashlib
import time

import psutil
import requests

def call_bt_status_api():
    api_sk="bu2DutNRkS5yFZTjlPni6sXFVh7LHkWh"
    request_time=str(int(time.time()))
    def md5(s:str):
        return hashlib.md5(s.encode('utf-8')).hexdigest()

    # hashlib.md5((request_time + hashlib.md5(api_sk.encode()).hexdigest()).encode()).hexdigest()
    # request_token = md5(str(request_time)+''+md5(api_sk))
    p_data = {
        # "action": "GetNetWork",
        'request_token': md5(request_time + md5(api_sk)),
        'request_time': request_time
    }
    x = requests.post(url="https://hk.yousb.top:8888/system?action=GetNetWork",data=p_data)
    try:
        res = x.json()
        return res
    except:
        return {
            "status": False,
            "msg": x.text
        }
def get_status():
    return {
        "cpu": psutil.cpu_percent(),
        "memory": psutil.virtual_memory().percent,
        "disk": {d.mountpoint: usage.percent
        for d in psutil.disk_partitions()
        if (usage := psutil.disk_usage(d.mountpoint))
                 },
        "swap": psutil.swap_memory().percent,
    }

def formatted(main_data: dict):
    """主格式化函数"""
    def format_size(byte_size):
        """将字节数转换为人类可读的格式"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if byte_size < 1024.0:
                return f"{byte_size:.2f} {unit}"
            byte_size /= 1024.0
        return f"{byte_size:.2f} PB"

    def format_network(network_data):
        """格式化网络接口信息"""
        output = ["=== 网络接口状态 ==="]

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
        output = ["=== 系统概览 ===", f"系统名称: {data['title']} | 运行时间: {data['time']}",
                  f"系统版本: {data['system']} | 宝塔版本: {data['version']}",
                  f"网站数量: {data['site_total']} | FTP账户: {data['ftp_total']} | 数据库: {data['database_total']}",
                  "-" * 50]
        return "\n".join(output)

    def format_cpu(data):
        """格式化CPU信息"""
        output = ["=== CPU状态 ==="]

        # 解析CPU信息（根据原始数据结构适配）
        cpu_info = data["cpu"]
        core_info = cpu_info[2]
        output.append(f"处理器型号: {cpu_info[3]}")
        output.append(f"逻辑核心数: {cpu_info[4]} | 线程数: {cpu_info[5]}")
        output.append(
            f"当前负载: 用户进程 {data['cpu_times']['user']:.1f} | 系统进程 {data['cpu_times']['system']:.1f}")
        output.append(f"空闲率: {data['cpu_times']['idle']:.1f}% | 总进程数: {data['cpu_times']['总进程数']}")
        output.append("-" * 50)
        return "\n".join(output)

    def format_memory(data):
        """格式化内存信息"""
        output = ["=== 内存状态 ==="]

        mem_total = format_size(data["mem"]["memTotal"] * 1024 ** 2)  # 原始数据单位转换
        mem_used = format_size(data["mem"]["memRealUsed"] * 1024 ** 2)
        mem_free = format_size(data["mem"]["memFree"] * 1024 ** 2)

        output.append(f"总内存: {mem_total} | 已用内存: {mem_used} | 空闲内存: {mem_free}")
        output.append(f"缓存内存: {format_size(data['mem']['memCached'] * 1024 ** 2)}")
        output.append(f"可用内存: {format_size(data['mem']['memAvailable'] * 1024 ** 2)}")
        output.append("-" * 50)
        return "\n".join(output)

    def format_disk(data):
        """格式化磁盘信息"""
        output = ["=== 磁盘状态 ==="]

        for disk in data["disk"]:
            total = format_size(disk["byte_size"][0])
            used = format_size(disk["byte_size"][0] - disk["byte_size"][2])
            percent = disk["size"][3]

            output.append(f"挂载点: {disk['path']} | 文件系统: {disk['filesystem']}")
            output.append(f"总空间: {total} | 已用空间: {used} | 使用率: {percent}")
            output.append(f"inode使用率: {disk['inodes'][3]}")
            output.append("-" * 50)

        return "\n".join(output)

    report = [format_system(main_data), format_cpu(main_data), format_memory(main_data), format_disk(main_data), format_network(main_data),
              "=== 系统负载 ===",
              f"1分钟负载: {main_data['load']['one']:.2f} | 5分钟负载: {main_data['load']['five']:.2f} | 15分钟负载: {main_data['load']['fifteen']:.2f}",
              f"负载阈值: {main_data['load']['safe']}/{main_data['load']['max']}"]
    return report

    # 添加负载信息