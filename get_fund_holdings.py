#!/usr/bin/env python3
"""
获取东吴移动互联基金(001323)2024-2025年季度前十大持股数据
"""

import requests
import json
from datetime import datetime
from typing import List, Dict

# 理杏仁API配置
TOKEN = "78bd45e6-300d-406d-974e-4ee3e49b59ba"
BASE_URL = "https://open.lixinger.com/api"


def get_fund_info(fund_codes: List[str]) -> Dict:
    """
    获取基金基本信息
    
    Args:
        fund_codes: 基金代码列表
    
    Returns:
        基金基本信息
    """
    url = f"{BASE_URL}/cn/fund/profile"
    
    data = {
        "token": TOKEN,
        "stockCodes": fund_codes
    }
    
    try:
        response = requests.post(url, json=data, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return {}


def get_fund_holdings(fund_code: str, start_date: str, end_date: str) -> Dict:
    """
    获取基金持仓数据
    
    Args:
        fund_code: 基金代码，如 "001323"
        start_date: 开始日期，格式 YYYY-MM-DD
        end_date: 结束日期，格式 YYYY-MM-DD
    
    Returns:
        API响应数据
    """
    url = f"{BASE_URL}/cn/fund/shareholdings"
    
    data = {
        "token": TOKEN,
        "stockCode": fund_code,
        "startDate": start_date,
        "endDate": end_date
    }
    
    try:
        response = requests.post(url, json=data, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return {}


def parse_date(date_str: str) -> str:
    """
    解析日期字符串，支持多种格式
    
    Args:
        date_str: 日期字符串
    
    Returns:
        标准格式 YYYY-MM-DD
    """
    if not date_str:
        return ""
    
    # 尝试解析 ISO 格式 (2025-12-31T00:00:00+08:00)
    if 'T' in date_str:
        try:
            dt = datetime.fromisoformat(date_str.replace('+08:00', ''))
            return dt.strftime('%Y-%m-%d')
        except:
            pass
    
    # 尝试标准格式
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return date_str
    except:
        pass
    
    return date_str


def analyze_holdings_by_quarter(holdings_data: List[Dict]) -> Dict:
    """
    按季度分析持仓数据
    
    Args:
        holdings_data: 持仓数据列表
    
    Returns:
        按季度分组的持仓数据
    """
    quarters = {}
    
    for holding in holdings_data:
        # 尝试多个可能的日期字段
        date_str = (holding.get('date') or 
                   holding.get('reportDate') or 
                   holding.get('publishDate') or '')
        
        date = parse_date(date_str)
        if not date:
            continue
        
        # 解析日期，确定季度
        try:
            dt = datetime.strptime(date, '%Y-%m-%d')
            year = dt.year
            month = dt.month
            
            # 确定季度
            if month <= 3:
                quarter = f"{year}Q1"
            elif month <= 6:
                quarter = f"{year}Q2"
            elif month <= 9:
                quarter = f"{year}Q3"
            else:
                quarter = f"{year}Q4"
            
            if quarter not in quarters:
                quarters[quarter] = []
            
            quarters[quarter].append({
                'date': date,
                'stock_name': holding.get('stockName', holding.get('name', '')),
                'stock_code': holding.get('stockCode', holding.get('code', '')),
                'holdings': holding.get('holdings', 0),
                'market_cap': holding.get('marketCap', holding.get('market_cap', 0)),
                'net_value_ratio': holding.get('netValueRatio', holding.get('net_value_ratio', 0)),
                'market_cap_ratio': holding.get('marketCapRatio', holding.get('market_cap_ratio', 0))
            })
        except Exception as e:
            print(f"解析日期失败: {date}, 错误: {e}")
            continue
    
    return quarters


def print_holdings_report(quarters: Dict):
    """
    打印持仓报告
    
    Args:
        quarters: 按季度分组的持仓数据
    """
    print("\n" + "="*80)
    print("东吴移动互联基金(001323) 季度前十大持股报告")
    print("="*80)
    
    # 按季度排序
    sorted_quarters = sorted(quarters.keys())
    
    for quarter in sorted_quarters:
        holdings = quarters[quarter]
        
        # 按持仓市值排序，取前10
        top10 = sorted(holdings, key=lambda x: x.get('market_cap', 0), reverse=True)[:10]
        
        print(f"\n📅 {quarter}")
        print("-"*80)
        print(f"{'排名':<4} {'股票代码':<10} {'股票名称':<15} {'持股数量':<12} {'持仓市值(万)':<15} {'占净值比':<10}")
        print("-"*80)
        
        for i, holding in enumerate(top10, 1):
            stock_code = holding.get('stock_code', '')
            stock_name = holding.get('stock_name', '')
            holdings_num = holding.get('holdings', 0)
            market_cap = holding.get('market_cap', 0) / 10000  # 转换为万
            net_value_ratio = holding.get('net_value_ratio', 0)
            if net_value_ratio < 1:  # 如果是小数，转换为百分比
                net_value_ratio = net_value_ratio * 100
            
            print(f"{i:<4} {stock_code:<10} {stock_name:<15} {holdings_num:<12.0f} {market_cap:<15.2f} {net_value_ratio:<10.2f}%")
        
        print()


def save_to_json(quarters: Dict, filename: str = "fund_holdings_001323.json"):
    """
    保存数据到JSON文件
    
    Args:
        quarters: 按季度分组的持仓数据
        filename: 文件名
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(quarters, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 数据已保存到: {filename}")


def main():
    """主函数"""
    fund_code = "001323"
    fund_name = "东吴移动互联"
    
    print(f"正在获取 {fund_name}({fund_code}) 的持仓数据...")
    print("时间范围: 2024-01-01 至 2025-12-31")
    
    # 获取基金基本信息
    print("\n1. 获取基金基本信息...")
    fund_info = get_fund_info([fund_code])
    if fund_info and 'data' in fund_info:
        info = fund_info['data'][0] if fund_info['data'] else {}
        print(f"   基金名称: {info.get('c_name', '')}")
        print(f"   基金类型: {info.get('op_mode', '')}")
        print(f"   成立日期: {info.get('inception_date', '')}")
        print(f"   管理公司: {info.get('f_c_name', '')}")
    else:
        print(f"   未能获取基金信息")
    
    # 获取持仓数据
    print("\n2. 获取持仓数据...")
    holdings_data = get_fund_holdings(fund_code, "2024-01-01", "2025-12-31")
    
    if not holdings_data or 'data' not in holdings_data:
        print("❌ 未获取到持仓数据")
        print(f"响应内容: {holdings_data}")
        return
    
    data = holdings_data.get('data', [])
    if not data:
        print("❌ 持仓数据为空")
        return
    
    print(f"   成功获取 {len(data)} 条持仓记录")
    
    # 显示第一条数据，了解数据结构
    print("\n3. 数据结构示例:")
    print(f"   {json.dumps(data[0], ensure_ascii=False, indent=2)[:500]}")
    
    # 按季度分析
    print("\n4. 按季度分析数据...")
    quarters = analyze_holdings_by_quarter(data)
    
    if not quarters:
        print("❌ 未能分析出季度数据")
        # 打印所有日期字段，帮助调试
        print("\n调试信息 - 所有记录的日期字段:")
        for i, item in enumerate(data[:5]):
            print(f"   记录{i+1}: date={item.get('date')}, reportDate={item.get('reportDate')}, publishDate={item.get('publishDate')}")
        return
    
    print(f"   共 {len(quarters)} 个季度")
    
    # 打印报告
    print_holdings_report(quarters)
    
    # 保存到文件
    save_to_json(quarters)
    
    print("\n" + "="*80)
    print("分析完成!")
    print("="*80)


if __name__ == "__main__":
    main()
