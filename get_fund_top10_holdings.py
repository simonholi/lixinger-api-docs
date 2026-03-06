#!/usr/bin/env python3
"""
获取东吴移动互联基金(001323)2024-2025年季度前十大持仓数据
展示每个季度末的前十大重仓股
"""

import requests
import json
from datetime import datetime
from typing import List, Dict

# 理杏仁API配置
TOKEN = "78bd45e6-300d-406d-974e-4ee3e49b59ba"
BASE_URL = "https://open.lixinger.com/api"


def get_fund_info(fund_codes: List[str]) -> Dict:
    """获取基金基本信息"""
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
    """获取基金持仓数据"""
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


def get_stock_info(stock_codes: List[str]) -> Dict:
    """获取股票基本信息（用于获取股票名称）"""
    url = f"{BASE_URL}/cn/company"
    data = {
        "token": TOKEN,
        "stockCodes": stock_codes
    }
    
    try:
        response = requests.post(url, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        # 构建股票代码到名称的映射
        stock_map = {}
        if 'data' in result:
            for item in result['data']:
                stock_map[item.get('stockCode', '')] = item.get('name', '')
        return stock_map
    except requests.exceptions.RequestException as e:
        print(f"获取股票信息失败: {e}")
        return {}


def parse_date(date_str: str) -> str:
    """解析日期字符串"""
    if not date_str:
        return ""
    
    # 尝试解析 ISO 格式
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


def get_quarter_from_date(date_str: str) -> str:
    """从日期获取季度"""
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        year = dt.year
        month = dt.month
        
        if month <= 3:
            return f"{year}Q1"
        elif month <= 6:
            return f"{year}Q2"
        elif month <= 9:
            return f"{year}Q3"
        else:
            return f"{year}Q4"
    except:
        return ""


def analyze_top10_holdings_by_quarter(holdings_data: List[Dict], stock_name_map: Dict = None) -> Dict:
    """
    按季度分析前十大持仓数据
    只取每个季度末的数据
    """
    quarters = {}
    
    for holding in holdings_data:
        # 获取日期
        date_str = holding.get('date', '')
        date = parse_date(date_str)
        if not date:
            continue
        
        quarter = get_quarter_from_date(date)
        if not quarter:
            continue
        
        # 只保留季度末的数据（3-31, 6-30, 9-30, 12-31）
        dt = datetime.strptime(date, '%Y-%m-%d')
        month = dt.month
        day = dt.day
        
        # 检查是否是季度末日期
        is_quarter_end = (
            (month == 3 and day == 31) or
            (month == 6 and day == 30) or
            (month == 9 and day == 30) or
            (month == 12 and day == 31)
        )
        
        if not is_quarter_end:
            continue
        
        if quarter not in quarters:
            quarters[quarter] = []
        
        stock_code = holding.get('stockCode', '')
        stock_name = holding.get('stockName', '')
        
        # 如果股票名称为空，从映射表中查找
        if not stock_name and stock_name_map and stock_code in stock_name_map:
            stock_name = stock_name_map[stock_code]
        
        quarters[quarter].append({
            'date': date,
            'stock_name': stock_name,
            'stock_code': stock_code,
            'holdings': holding.get('holdings', 0),
            'market_cap': holding.get('marketCap', 0),
            'net_value_ratio': holding.get('netValueRatio', 0),
            'stock_area_code': holding.get('stockAreaCode', '')
        })
    
    # 对每个季度的持仓按市值排序，取前10
    for quarter in quarters:
        # 按持仓市值降序排序
        sorted_holdings = sorted(quarters[quarter], key=lambda x: x['market_cap'], reverse=True)
        # 取前10
        top10 = sorted_holdings[:10]
        # 添加排名
        for i, holding in enumerate(top10, 1):
            holding['rank'] = i
        quarters[quarter] = top10
    
    return quarters


def print_top10_holdings_report(quarters: Dict):
    """打印前十大持仓报告"""
    print("\n" + "="*110)
    print("东吴移动互联基金(001323) 季度前十大持仓报告")
    print("="*110)
    
    # 按季度排序
    sorted_quarters = sorted(quarters.keys())
    
    for quarter in sorted_quarters:
        holdings = quarters[quarter]
        
        print(f"\n📅 {quarter} (报告日期: {holdings[0]['date'] if holdings else 'N/A'})")
        print("-"*110)
        print(f"{'排名':<6} {'股票代码':<12} {'股票名称':<20} {'持股数量':<16} {'持仓市值(万)':<18} {'占净值比':<12}")
        print("-"*110)
        
        for holding in holdings:
            rank = holding.get('rank', 0)
            stock_code = holding.get('stock_code', '')
            stock_name = holding.get('stock_name', '')
            holdings_num = holding.get('holdings', 0)
            market_cap = holding.get('market_cap', 0) / 10000  # 转换为万
            net_value_ratio = holding.get('net_value_ratio', 0)
            if net_value_ratio < 1:
                net_value_ratio = net_value_ratio * 100
            
            print(f"{rank:<6} {stock_code:<12} {stock_name:<20} {holdings_num:<16.0f} {market_cap:<18.2f} {net_value_ratio:<12.2f}%")
        
        print()


def save_to_json(quarters: Dict, filename: str = "fund_top10_holdings_001323.json"):
    """保存数据到JSON文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(quarters, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 数据已保存到: {filename}")


def save_to_excel(quarters: Dict, filename: str = "fund_top10_holdings_001323.xlsx"):
    """保存数据到Excel文件"""
    try:
        import pandas as pd
        
        # 准备数据
        all_data = []
        for quarter in sorted(quarters.keys()):
            for holding in quarters[quarter]:
                all_data.append({
                    '季度': quarter,
                    '报告日期': holding['date'],
                    '排名': holding['rank'],
                    '股票代码': holding['stock_code'],
                    '股票名称': holding['stock_name'],
                    '持股数量': holding['holdings'],
                    '持仓市值(万)': holding['market_cap'] / 10000,
                    '占净值比(%)': holding['net_value_ratio'] * 100 if holding['net_value_ratio'] < 1 else holding['net_value_ratio']
                })
        
        df = pd.DataFrame(all_data)
        df.to_excel(filename, index=False, engine='openpyxl')
        print(f"✅ Excel数据已保存到: {filename}")
    except ImportError:
        print("⚠️ 未安装 pandas 和 openpyxl，无法生成Excel文件")
        print("   请运行: pip install pandas openpyxl")


def main():
    """主函数"""
    fund_code = "001323"
    fund_name = "东吴移动互联"
    
    print(f"正在获取 {fund_name}({fund_code}) 的季度前十大持仓数据...")
    print("时间范围: 2024-01-01 至 2025-12-31")
    print("说明: 只获取每个季度末(3-31, 6-30, 9-30, 12-31)的前十大重仓股")
    
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
    
    # 收集所有股票代码，用于查询股票名称
    print("\n3. 获取股票名称信息...")
    stock_codes = list(set([h.get('stockCode', '') for h in data if h.get('stockCode')]))
    print(f"   共 {len(stock_codes)} 只不同股票")
    stock_name_map = get_stock_info(stock_codes)
    print(f"   成功获取 {len(stock_name_map)} 只股票名称")
    
    # 按季度分析前十大持仓
    print("\n4. 按季度分析前十大持仓数据...")
    quarters = analyze_top10_holdings_by_quarter(data, stock_name_map)
    
    if not quarters:
        print("❌ 未能分析出季度数据")
        return
    
    print(f"   共 {len(quarters)} 个季度")
    
    # 打印报告
    print_top10_holdings_report(quarters)
    
    # 保存到文件
    save_to_json(quarters)
    save_to_excel(quarters)
    
    print("\n" + "="*110)
    print("分析完成!")
    print("="*110)


if __name__ == "__main__":
    main()
