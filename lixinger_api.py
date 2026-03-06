#!/usr/bin/env python3
"""
理杏仁 API Python 接口
类似 akshare 的调用方式
"""

import requests
import json
from typing import Dict, List, Optional, Union
from dataclasses import dataclass


@dataclass
class LixingerConfig:
    """理杏仁配置"""
    token: str
    base_url: str = "https://open.lixinger.com/api"
    
    
class LixingerAPI:
    """
    理杏仁 API 调用类
    
    使用示例:
        from lixinger_api import LixingerAPI
        
        # 初始化
        api = LixingerAPI(token="your_token_here")
        
        # 获取基本面数据
        data = api.get_fundamental(
            stock_codes=["300750", "600519"],
            metrics_list=["pe_ttm", "pb", "mc"]
        )
    """
    
    def __init__(self, token: str):
        """
        初始化理杏仁 API
        
        Args:
            token: 你的理杏仁 API Token
        """
        self.config = LixingerConfig(token=token)
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def _post(self, endpoint: str, data: Dict) -> Dict:
        """
        发送 POST 请求
        
        Args:
            endpoint: API 端点路径
            data: 请求数据
            
        Returns:
            API 响应数据
        """
        url = f"{self.config.base_url}{endpoint}"
        
        # 添加 token
        data['token'] = self.config.token
        
        try:
            response = self.session.post(url, json=data, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"请求失败: {e}")
    
    # ==================== 公司接口 ====================
    
    def get_company_fundamental(self, 
                                 stock_codes: List[str],
                                 metrics_list: List[str],
                                 date: Optional[str] = None,
                                 start_date: Optional[str] = None,
                                 end_date: Optional[str] = None,
                                 limit: Optional[int] = None) -> Dict:
        """
        获取公司基本面数据（非金融类）
        
        Args:
            stock_codes: 股票代码列表，如 ["300750", "600519"]
            metrics_list: 指标列表，如 ["pe_ttm", "pb", "mc"]
            date: 指定日期，格式 YYYY-MM-DD
            start_date: 开始日期，格式 YYYY-MM-DD
            end_date: 结束日期，格式 YYYY-MM-DD
            limit: 返回最近数据的数量
            
        Returns:
            基本面数据
            
        示例:
            api.get_company_fundamental(
                stock_codes=["300750", "600519"],
                metrics_list=["pe_ttm", "pb", "mc"],
                date="2024-01-01"
            )
        """
        data = {
            "stockCodes": stock_codes,
            "metricsList": metrics_list
        }
        
        if date:
            data["date"] = date
        if start_date:
            data["startDate"] = start_date
        if end_date:
            data["endDate"] = end_date
        if limit:
            data["limit"] = limit
            
        return self._post("/cn/company/fundamental/non_financial", data)
    
    def get_company_profile(self, stock_codes: List[str]) -> Dict:
        """
        获取公司概况
        
        Args:
            stock_codes: 股票代码列表
            
        Returns:
            公司概况数据
        """
        data = {
            "stockCodes": stock_codes
        }
        return self._post("/cn/company/profile", data)
    
    def get_company_candlestick(self,
                                 stock_codes: List[str],
                                 date: Optional[str] = None,
                                 start_date: Optional[str] = None,
                                 end_date: Optional[str] = None,
                                 fq: Optional[str] = None) -> Dict:
        """
        获取 K 线数据
        
        Args:
            stock_codes: 股票代码列表
            date: 指定日期
            start_date: 开始日期
            end_date: 结束日期
            fq: 复权类型，可选 "pre"(前复权)、"post"(后复权)、None(不复权)
            
        Returns:
            K 线数据
        """
        data = {
            "stockCodes": stock_codes
        }
        
        if date:
            data["date"] = date
        if start_date:
            data["startDate"] = start_date
        if end_date:
            data["endDate"] = end_date
        if fq:
            data["fq"] = fq
            
        return self._post("/cn/company/candlestick", data)
    
    def get_company_shareholders(self, stock_codes: List[str]) -> Dict:
        """
        获取股东人数数据
        
        Args:
            stock_codes: 股票代码列表
            
        Returns:
            股东人数数据
        """
        data = {
            "stockCodes": stock_codes
        }
        return self._post("/cn/company/shareholders-num", data)
    
    # ==================== 基金接口 ====================
    
    def get_fund_profile(self, fund_codes: List[str]) -> Dict:
        """
        获取基金概况
        
        Args:
            fund_codes: 基金代码列表，如 ["110022", "160106"]
            
        Returns:
            基金概况数据
        """
        data = {
            "fundCodes": fund_codes
        }
        return self._post("/cn/fund/profile", data)
    
    def get_fund_net_value(self,
                           fund_codes: List[str],
                           date: Optional[str] = None,
                           start_date: Optional[str] = None,
                           end_date: Optional[str] = None) -> Dict:
        """
        获取基金净值
        
        Args:
            fund_codes: 基金代码列表
            date: 指定日期
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            基金净值数据
        """
        data = {
            "fundCodes": fund_codes
        }
        
        if date:
            data["date"] = date
        if start_date:
            data["startDate"] = start_date
        if end_date:
            data["endDate"] = end_date
            
        return self._post("/cn/fund/net-value", data)
    
    # ==================== 指数接口 ====================
    
    def get_index_constituents(self, index_code: str) -> Dict:
        """
        获取指数成分股
        
        Args:
            index_code: 指数代码，如 "000300"(沪深300)
            
        Returns:
            指数成分股数据
        """
        data = {
            "indexCode": index_code
        }
        return self._post("/cn/index/constituents", data)
    
    def get_index_candlestick(self,
                              index_codes: List[str],
                              date: Optional[str] = None,
                              start_date: Optional[str] = None,
                              end_date: Optional[str] = None) -> Dict:
        """
        获取指数 K 线数据
        
        Args:
            index_codes: 指数代码列表
            date: 指定日期
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            指数 K 线数据
        """
        data = {
            "indexCodes": index_codes
        }
        
        if date:
            data["date"] = date
        if start_date:
            data["startDate"] = start_date
        if end_date:
            data["endDate"] = end_date
            
        return self._post("/cn/company/candlestick", data)
    
    # ==================== 宏观接口 ====================
    
    def get_macro_gdp(self) -> Dict:
        """
        获取 GDP 数据
        
        Returns:
            GDP 数据
        """
        data = {}
        return self._post("/macro/gdp", data)
    
    def get_macro_cpi(self) -> Dict:
        """
        获取 CPI 数据
        
        Returns:
            CPI 数据
        """
        data = {}
        return self._post("/macro/cpi", data)
    
    def get_macro_interest_rates(self) -> Dict:
        """
        获取利率数据
        
        Returns:
            利率数据
        """
        data = {}
        return self._post("/macro/interest-rates", data)


# ==================== 便捷函数 ====================

def get_fundamental(token: str,
                    stock_codes: List[str],
                    metrics_list: List[str],
                    date: Optional[str] = None) -> Dict:
    """
    便捷函数：获取基本面数据
    
    Args:
        token: API Token
        stock_codes: 股票代码列表
        metrics_list: 指标列表
        date: 指定日期
        
    Returns:
        基本面数据
        
    示例:
        import lixinger_api as lx
        
        data = lx.get_fundamental(
            token="your_token",
            stock_codes=["300750", "600519"],
            metrics_list=["pe_ttm", "pb", "mc"],
            date="2024-01-01"
        )
    """
    api = LixingerAPI(token=token)
    return api.get_company_fundamental(
        stock_codes=stock_codes,
        metrics_list=metrics_list,
        date=date
    )


if __name__ == "__main__":
    # 使用示例
    print("理杏仁 API Python 接口")
    print("=" * 50)
    print("\n使用示例:")
    print("-" * 50)
    print("""
from lixinger_api import LixingerAPI

# 初始化 API
api = LixingerAPI(token="your_token_here")

# 获取基本面数据
data = api.get_company_fundamental(
    stock_codes=["300750", "600519"],
    metrics_list=["pe_ttm", "pb", "mc"],
    date="2024-01-01"
)

print(data)
    """)
    print("-" * 50)
